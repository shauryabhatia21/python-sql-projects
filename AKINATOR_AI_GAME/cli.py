"""
Akinator CLI Terminal Game
Interactive, colored terminal interface for the Python Akinator engine.
"""

import sys
import time
from engine import AkinatorEngine, ANSWERS

# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
WHITE = "\033[97m"

GENIE_BANNER = rf"""{CYAN}{BOLD}
          .---.
         /     \
        | () () |       ___   _  ___ _   _    _  _____ ___  ____
         \  -  /       / _ \ | |/ / | \ | |  / \|_   _/ _ \|  _ \
         /'-.-'\      / /_\ \| ' /| |  \| | / _ \ | || | | | |_) |
        / /| |\ \     |  _  || . \| | |\  |/ ___ \| || |_| |  _ <
       /_/ |_| \_\    |_| |_||_|\_\_|_| \_/_/   \_\_| \___/|_| \_\
         ||   ||
         ()   ()          {YELLOW}The Web Genius - Python Edition{CYAN}
{RESET}"""

def render_meter(probability: float, length: int = 24) -> str:
    filled = int(round(probability * length))
    bar = "█" * filled + "░" * (length - filled)
    percent = int(probability * 100)
    color = GREEN if percent >= 75 else YELLOW if percent >= 40 else CYAN
    return f"{color}[{bar}] {percent}%{RESET}"

def print_separator():
    print(f"{BLUE}────────────────────────────────────────────────────────────────────────{RESET}")

def run_cli():
    # Enable UTF-8 and ANSI escape processing in Windows console
    if sys.platform == "win32":
        import os
        os.system("color")
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print(GENIE_BANNER)
    print(f"{MAGENTA}{BOLD}Think about a real or fictional character. I will try to guess who it is!{RESET}\n")

    engine = AkinatorEngine()

    while True:
        engine.reset()
        print(f"{YELLOW}Knowledge base loaded with {len(engine.characters)} characters and {len(engine.questions)} questions.{RESET}")
        input(f"\n{BOLD}Press [ENTER] when you are ready with your character in mind...{RESET}")
        print()

        while True:
            # Check if Akinator wants to make a guess
            if engine.should_make_guess():
                top_char, top_prob = engine.get_top_candidate()
                if top_char:
                    print_separator()
                    print(f"\n{YELLOW}{BOLD}✨ I think you are thinking of...{RESET}")
                    print(f"\n   🔮 {GREEN}{BOLD}{top_char['name']}{RESET}")
                    if top_char.get("description"):
                        print(f"      {CYAN}{top_char['description']}{RESET}\n")

                    while True:
                        ans = input(f"{BOLD}Am I right? [y/n]: {RESET}").strip().lower()
                        if ans in ["y", "yes"]:
                            print(f"\n{GREEN}{BOLD}🎉 Hooray! Akinator guessed right once more!{RESET}")
                            print(f"{MAGENTA}Thanks for playing!{RESET}\n")
                            break
                        elif ans in ["n", "no"]:
                            engine.reject_current_guess()
                            # Check if we still have questions and characters to try
                            rem_char, rem_prob = engine.get_top_candidate()
                            unasked = [q for q in engine.questions if q["id"] not in engine.asked_questions]
                            if rem_char and unasked and len(engine.asked_questions) < 22:
                                print(f"\n{YELLOW}Hmm... let me dig deeper!{RESET}\n")
                                break
                            else:
                                # Akinator gives up -> Learning mode!
                                print_separator()
                                print(f"\n{RED}{BOLD}💥 Bravo! You defeated me! I give up!{RESET}")
                                print(f"{CYAN}Help me learn who you were thinking of so I get smarter!{RESET}\n")

                                while True:
                                    correct_name = input(f"{BOLD}Who was your character? {RESET}").strip()
                                    if correct_name:
                                        break

                                correct_desc = input(f"{BOLD}Short description (optional): {RESET}").strip()

                                print(f"\nEnter a question that differentiates {BOLD}{correct_name}{RESET} from {BOLD}{top_char['name']}{RESET}:")
                                print(f"{YELLOW}(Example: Does your character wear a red cape?){RESET}")
                                while True:
                                    diff_question = input(f"{BOLD}Question: {RESET}").strip()
                                    if diff_question:
                                        if not diff_question.endswith("?"):
                                            diff_question += "?"
                                        break

                                while True:
                                    q_ans = input(f"{BOLD}What would the answer be for {correct_name}? [yes/no]: {RESET}").strip().lower()
                                    if q_ans in ["y", "yes"]:
                                        new_ans = 1.0
                                        rej_ans = 0.0
                                        break
                                    elif q_ans in ["n", "no"]:
                                        new_ans = 0.0
                                        rej_ans = 1.0
                                        break

                                engine.learn_character(
                                    name=correct_name,
                                    description=correct_desc,
                                    new_question_text=diff_question,
                                    answer_for_new=new_ans,
                                    answer_for_rejected=rej_ans,
                                    rejected_char_id=top_char["id"]
                                )
                                print(f"\n{GREEN}{BOLD}✨ Thank you! I have saved '{correct_name}' into my memory.{RESET}\n")
                                break
                        else:
                            print("Please answer with 'y' or 'n'.")

                    if ans in ["y", "yes"] or not (rem_char and unasked and len(engine.asked_questions) < 22):
                        break

            # Get next best question
            q = engine.get_best_question()
            if not q:
                # No more questions, force guess
                top_char, _ = engine.get_top_candidate()
                if top_char:
                    print_separator()
                    print(f"\n{YELLOW}{BOLD}I have asked all my questions! Is your character {top_char['name']}?{RESET}")
                break

            q_num = len(engine.asked_questions) + 1
            _, top_prob = engine.get_top_candidate()

            print_separator()
            print(f"{CYAN}{BOLD}Question {q_num}{RESET}  |  Confidence: {render_meter(top_prob)}")
            print(f"\n  {WHITE}{BOLD}▶ {q['text']}{RESET}\n")
            print(f"  {GREEN}[1] Yes{RESET}          {BLUE}[2] Probably{RESET}       {WHITE}[3] Don't Know{RESET}")
            print(f"  {YELLOW}[4] Probably Not{RESET} {RED}[5] No{RESET}             {MAGENTA}[U] Undo last{RESET}   [Q] Quit")
            print()

            while True:
                choice = input(f"{BOLD}Your answer (1-5 / U / Q): {RESET}").strip().lower()
                if choice in ["1", "yes", "y"]:
                    engine.submit_answer(q["id"], ANSWERS["YES"])
                    break
                elif choice in ["2", "probably", "p"]:
                    engine.submit_answer(q["id"], ANSWERS["PROBABLY"])
                    break
                elif choice in ["3", "don't know", "dont know", "d"]:
                    engine.submit_answer(q["id"], ANSWERS["DONT_KNOW"])
                    break
                elif choice in ["4", "probably not", "pn"]:
                    engine.submit_answer(q["id"], ANSWERS["PROBABLY_NOT"])
                    break
                elif choice in ["5", "no", "n"]:
                    engine.submit_answer(q["id"], ANSWERS["NO"])
                    break
                elif choice in ["u", "undo"]:
                    if engine.undo():
                        print(f"{YELLOW}Reverted last answer.{RESET}")
                    else:
                        print(f"{RED}No previous question to undo.{RESET}")
                    break
                elif choice in ["q", "quit", "exit"]:
                    print(f"\n{CYAN}Goodbye! Thanks for playing Akinator!{RESET}")
                    return
                else:
                    print(f"{RED}Invalid input. Please enter 1, 2, 3, 4, 5, U, or Q.{RESET}")

        # Ask to play again
        print_separator()
        again = input(f"{BOLD}Would you like to play again? [y/n]: {RESET}").strip().lower()
        if again not in ["y", "yes"]:
            print(f"\n{CYAN}See you next time! Farewell! 🧞✨{RESET}\n")
            break

if __name__ == "__main__":
    run_cli()
