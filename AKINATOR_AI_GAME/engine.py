"""
Akinator AI Engine
Handles information-entropy question selection, Bayesian likelihood scoring,
history/undo management, and persistent self-learning.
"""

import json
import math
import os
from typing import Dict, List, Optional, Tuple

ANSWERS = {
    "YES": 1.0,
    "PROBABLY": 0.75,
    "DONT_KNOW": 0.5,
    "PROBABLY_NOT": 0.25,
    "NO": 0.0,
}

ANSWER_LABELS = {
    1.0: "Yes",
    0.75: "Probably",
    0.5: "Don't Know",
    0.25: "Probably Not",
    0.0: "No",
}


class AkinatorEngine:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), "akinator_db.json")
        self.db_path = os.path.abspath(db_path)
        self.load_database()
        self.reset()

    def load_database(self):
        """Load questions and characters from the JSON database."""
        with open(self.db_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.questions: List[Dict] = data.get("questions", [])
        self.characters: List[Dict] = data.get("characters", [])
        self.questions_by_id = {q["id"]: q for q in self.questions}
        self.characters_by_id = {c["id"]: c for c in self.characters}

    def save_database(self):
        """Save the updated knowledge base back to the JSON file."""
        data = {
            "questions": self.questions,
            "characters": self.characters,
        }
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def reset(self):
        """Reset the game state for a new round."""
        self.asked_questions: List[str] = []
        self.history: List[Tuple[str, float, Dict[str, float]]] = []
        self.ignored_guesses: List[str] = []  # IDs of characters the user already rejected this session

        # Uniform prior probability
        n = len(self.characters)
        if n > 0:
            self.probabilities: Dict[str, float] = {c["id"]: 1.0 / n for c in self.characters}
        else:
            self.probabilities = {}

    def get_character_answer(self, character: Dict, question_id: str) -> float:
        """Get character's known answer for a question, default 0.5 (unknown)."""
        return character.get("answers", {}).get(question_id, 0.5)

    def get_top_candidate(self) -> Tuple[Optional[Dict], float]:
        """Return the most likely character and its probability (0.0 to 1.0)."""
        candidates = {
            cid: prob for cid, prob in self.probabilities.items()
            if cid not in self.ignored_guesses
        }
        if not candidates:
            return None, 0.0

        best_id = max(candidates, key=candidates.get)
        best_prob = candidates[best_id]
        return self.characters_by_id.get(best_id), best_prob

    def get_top_candidates_list(self, top_n: int = 5) -> List[Tuple[Dict, float]]:
        """Return top N candidates ranked by probability."""
        candidates = [
            (self.characters_by_id[cid], prob)
            for cid, prob in self.probabilities.items()
            if cid in self.characters_by_id and cid not in self.ignored_guesses
        ]
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_n]

    def should_make_guess(self, min_questions: int = 5, max_questions: int = 25, threshold: float = 0.80) -> bool:
        """Decide whether Akinator is confident enough or has exhausted questions to guess."""
        questions_count = len(self.asked_questions)
        top_char, top_prob = self.get_top_candidate()

        if not top_char:
            return False

        # If confident after at least min_questions
        if questions_count >= min_questions and top_prob >= threshold:
            return True

        # If reached question cap or no more questions to ask
        unasked = [q["id"] for q in self.questions if q["id"] not in self.asked_questions]
        if questions_count >= max_questions or not unasked:
            return True

        return False

    def get_best_question(self) -> Optional[Dict]:
        """
        Pick the unasked question that maximizes information gain (variance across probable candidates).
        This seeks questions that split the remaining candidate pool evenly (~50/50).
        """
        unasked = [q for q in self.questions if q["id"] not in self.asked_questions]
        if not unasked:
            return None

        # Filter candidates that still hold meaningful probability
        active_candidates = [
            (c, self.probabilities.get(c["id"], 0.0))
            for c in self.characters
            if c["id"] not in self.ignored_guesses and self.probabilities.get(c["id"], 0.0) > 0.001
        ]

        if not active_candidates:
            return unasked[0]

        total_prob = sum(p for _, p in active_candidates)
        if total_prob == 0:
            return unasked[0]

        best_q = None
        best_score = -1.0

        for q in unasked:
            qid = q["id"]

            # Expected answer value across candidates
            mean_answer = sum(
                (p / total_prob) * self.get_character_answer(c, qid)
                for c, p in active_candidates
            )

            # Variance: higher variance means the question divides the candidates strongly
            variance = sum(
                (p / total_prob) * ((self.get_character_answer(c, qid) - mean_answer) ** 2)
                for c, p in active_candidates
            )

            # Bonus score for questions where mean is close to 0.5 (even split)
            balance = 1.0 - 2.0 * abs(mean_answer - 0.5)
            score = variance * 0.7 + balance * 0.3

            if score > best_score:
                best_score = score
                best_q = q

        return best_q if best_q else unasked[0]

    def submit_answer(self, question_id: str, user_answer: float):
        """
        Update probabilities based on user answer.
        user_answer: 1.0 (Yes), 0.75 (Probably), 0.5 (Don't Know), 0.25 (Probably Not), 0.0 (No)
        """
        # Save current state in history for Undo
        self.history.append((question_id, user_answer, dict(self.probabilities)))
        self.asked_questions.append(question_id)

        # If the user says "Don't know" (0.5), we don't penalize characters strongly
        if user_answer == 0.5:
            return

        # Likelihood function: Gaussian drop-off based on distance between answer and character expectation
        for cid, char in self.characters_by_id.items():
            expected = self.get_character_answer(char, question_id)
            distance = abs(user_answer - expected)

            # Exponential decay: exact match -> 1.0, close -> ~0.83, opposite -> ~0.05
            likelihood = math.exp(-3.2 * (distance ** 2))
            likelihood = max(likelihood, 0.02)  # avoid absolute zero

            self.probabilities[cid] = self.probabilities.get(cid, 0.0) * likelihood

        # Normalize probabilities
        total = sum(self.probabilities.values())
        if total > 0:
            for cid in self.probabilities:
                self.probabilities[cid] /= total

    def undo(self) -> bool:
        """Revert the last question and restore previous probabilities."""
        if not self.history:
            return False

        last_qid, _, prev_probs = self.history.pop()
        if last_qid in self.asked_questions:
            self.asked_questions.remove(last_qid)

        self.probabilities = prev_probs
        return True

    def reject_current_guess(self):
        """User stated Akinator's guess was incorrect."""
        top_char, _ = self.get_top_candidate()
        if top_char:
            self.ignored_guesses.append(top_char["id"])

        # Re-normalize among remaining
        candidates = {
            cid: p for cid, p in self.probabilities.items()
            if cid not in self.ignored_guesses
        }
        total = sum(candidates.values())
        if total > 0:
            for cid in self.probabilities:
                if cid in candidates:
                    self.probabilities[cid] /= total
                else:
                    self.probabilities[cid] = 0.0

    def learn_character(
        self,
        name: str,
        description: str,
        new_question_text: str,
        answer_for_new: float,
        answer_for_rejected: float = 0.0,
        rejected_char_id: Optional[str] = None
    ) -> Dict:
        """
        Add a new character and distinguishing question to the knowledge base.
        Saves immediately to akinator_db.json.
        """
        # 1. Create or find question ID
        existing_q = next((q for q in self.questions if q["text"].strip().lower() == new_question_text.strip().lower()), None)
        if existing_q:
            qid = existing_q["id"]
        else:
            qid = f"q{len(self.questions) + 1}"
            new_q = {"id": qid, "text": new_question_text.strip()}
            self.questions.append(new_q)
            self.questions_by_id[qid] = new_q

        # 2. Collect answers the user gave in this session
        session_answers = {}
        for q_id, u_ans, _ in self.history:
            session_answers[q_id] = u_ans
        session_answers[qid] = answer_for_new

        # 3. Create new character
        new_cid = f"c{len(self.characters) + 1}"
        new_character = {
            "id": new_cid,
            "name": name.strip(),
            "description": description.strip() if description else "Custom learned character.",
            "answers": session_answers,
        }
        self.characters.append(new_character)
        self.characters_by_id[new_cid] = new_character

        # 4. Update the rejected character's answer to this new question if known
        if rejected_char_id and rejected_char_id in self.characters_by_id:
            rej_char = self.characters_by_id[rejected_char_id]
            if "answers" not in rej_char:
                rej_char["answers"] = {}
            rej_char["answers"][qid] = answer_for_rejected

        # 5. Persist to disk
        self.save_database()
        return new_character
