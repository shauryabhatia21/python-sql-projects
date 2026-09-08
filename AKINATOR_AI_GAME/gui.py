"""
Akinator Desktop GUI (Tkinter + Canvas Art)
Features:
- Dynamic Genie expressions (Thinking, Confident, Guessing, Defeated)
- Live confidence progress meter
- 5-point fuzzy response buttons with hover highlights
- Undo support
- Guess verification modal
- Interactive Learning dialog to expand the knowledge base
"""

import math
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from engine import AkinatorEngine, ANSWERS

# Color Palette (Akinator Royal Purple / Midnight Gold)
BG_DARK = "#110e24"
BG_CARD = "#1c183b"
BG_HEADER = "#15122e"
GOLD = "#f5b041"
GOLD_HOVER = "#f8c471"
CYAN = "#00d2d3"
PURPLE_LIGHT = "#9980FA"
TEXT_WHITE = "#ffffff"
TEXT_MUTED = "#a4b0be"

COLOR_YES = "#10ac84"
COLOR_YES_HOVER = "#1dd1a1"
COLOR_PROB = "#0984e3"
COLOR_PROB_HOVER = "#74b9ff"
COLOR_DONTKNOW = "#57606f"
COLOR_DONTKNOW_HOVER = "#747d8c"
COLOR_PROBNOT = "#e67e22"
COLOR_PROBNOT_HOVER = "#f39c12"
COLOR_NO = "#eb4d4b"
COLOR_NO_HOVER = "#ff7979"


class GenieCanvas(tk.Canvas):
    """Draws a stylized, expressive Genie on a canvas with changing moods."""

    def __init__(self, master, width=220, height=220, **kwargs):
        super().__init__(master, width=width, height=height, bg=BG_CARD, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.mood = "thinking"  # "thinking", "confident", "guessing", "defeated"
        self.smoke_phase = 0
        self.draw()

    def set_mood(self, mood: str):
        self.mood = mood
        self.draw()

    def draw(self):
        self.delete("all")
        cx, cy = self.width // 2, self.height // 2 + 10

        # Mystical smoke/swirls at bottom
        self.create_oval(cx - 55, cy + 50, cx + 55, cy + 85, fill="#5f27cd", outline="")
        self.create_oval(cx - 75, cy + 62, cx + 75, cy + 95, fill="#341f97", outline="")

        # Glowing aura
        aura_color = "#f9ca24" if self.mood == "guessing" else "#70a1ff" if self.mood == "confident" else "#9980FA"
        self.create_oval(cx - 70, cy - 80, cx + 70, cy + 50, outline=aura_color, width=3)

        # Genie Body / Chest
        self.create_polygon(
            cx - 45, cy + 60,
            cx + 45, cy + 60,
            cx + 35, cy + 10,
            cx - 35, cy + 10,
            fill="#3498db", outline="#2980b9", width=2
        )
        # Gold collar/necklace
        self.create_arc(cx - 26, cy + 5, cx + 26, cy + 28, start=180, extent=180, fill=GOLD, outline="#d68910", width=2)

        # Head (Blue skin)
        self.create_oval(cx - 38, cy - 50, cx + 38, cy + 15, fill="#54a0ff", outline="#2e86de", width=2)

        # Ears & Gold Hoop Earring
        self.create_oval(cx - 45, cy - 25, cx - 35, cy - 10, fill="#54a0ff", outline="#2e86de")
        self.create_oval(cx + 35, cy - 25, cx + 45, cy - 10, fill="#54a0ff", outline="#2e86de")
        # Gold earring on left
        self.create_oval(cx - 44, cy - 13, cx - 36, cy - 3, outline=GOLD, width=3)

        # Turban (Royal purple with gold trim & cyan gemstone)
        self.create_oval(cx - 42, cy - 78, cx + 42, cy - 32, fill="#5f27cd", outline="#341f97", width=2)
        self.create_oval(cx - 35, cy - 70, cx + 35, cy - 40, fill="#6c5ce7", outline="")
        # Turban gem & feather
        self.create_line(cx, cy - 70, cx - 6, cy - 88, fill="#ffffff", width=3)
        self.create_oval(cx - 10, cy - 60, cx + 10, cy - 40, fill=GOLD, outline="#b7791f", width=2)
        self.create_oval(cx - 5, cy - 55, cx + 5, cy - 45, fill=CYAN, outline="")

        # Facial Features based on MOOD
        if self.mood == "thinking":
            # Thoughtful eyebrows
            self.create_line(cx - 24, cy - 22, cx - 8, cy - 26, width=3, fill="#1e272e")
            self.create_line(cx + 8, cy - 28, cx + 24, cy - 20, width=3, fill="#1e272e")
            # Eyes looking slightly up/side
            self.create_oval(cx - 22, cy - 20, cx - 10, cy - 8, fill="white", outline="#1e272e")
            self.create_oval(cx + 10, cy - 20, cx + 22, cy - 8, fill="white", outline="#1e272e")
            self.create_oval(cx - 17, cy - 18, cx - 12, cy - 11, fill="#1e272e")  # pupil up
            self.create_oval(cx + 15, cy - 18, cx + 20, cy - 11, fill="#1e272e")
            # Subtle smirk / stroke beard
            self.create_arc(cx - 10, cy - 5, cx + 10, cy + 8, start=190, extent=160, style="arc", width=2)
            # Pointy beard
            self.create_polygon(cx - 10, cy + 12, cx + 10, cy + 12, cx, cy + 28, fill="#1e272e")

        elif self.mood == "confident":
            # Confident sharp eyebrows
            self.create_line(cx - 24, cy - 27, cx - 8, cy - 21, width=3, fill="#1e272e")
            self.create_line(cx + 8, cy - 21, cx + 24, cy - 27, width=3, fill="#1e272e")
            # Normal open eyes
            self.create_oval(cx - 22, cy - 20, cx - 10, cy - 8, fill="white", outline="#1e272e")
            self.create_oval(cx + 10, cy - 20, cx + 22, cy - 8, fill="white", outline="#1e272e")
            self.create_oval(cx - 18, cy - 16, cx - 13, cy - 10, fill="#1e272e")
            self.create_oval(cx + 13, cy - 16, cx + 18, cy - 10, fill="#1e272e")
            # Smug broad smile
            self.create_arc(cx - 15, cy - 8, cx + 15, cy + 10, start=190, extent=160, fill="#ffffff", outline="#1e272e", width=2)
            # Pointy beard
            self.create_polygon(cx - 10, cy + 12, cx + 10, cy + 12, cx, cy + 28, fill="#1e272e")

        elif self.mood == "guessing":
            # Triumphant arched brows
            self.create_line(cx - 24, cy - 28, cx - 8, cy - 24, width=3, fill="#1e272e")
            self.create_line(cx + 8, cy - 24, cx + 24, cy - 28, width=3, fill="#1e272e")
            # Big sparkling happy eyes
            self.create_oval(cx - 23, cy - 22, cx - 9, cy - 6, fill="white", outline="#1e272e")
            self.create_oval(cx + 9, cy - 22, cx + 23, cy - 6, fill="white", outline="#1e272e")
            self.create_oval(cx - 18, cy - 17, cx - 12, cy - 9, fill="#0984e3")
            self.create_oval(cx + 14, cy - 17, cx + 20, cy - 9, fill="#0984e3")
            # Huge confident smile
            self.create_arc(cx - 18, cy - 8, cx + 18, cy + 14, start=190, extent=160, fill="#ffffff", outline="#1e272e", width=2)
            self.create_polygon(cx - 10, cy + 14, cx + 10, cy + 14, cx, cy + 30, fill="#1e272e")
            # Magic stars near head
            self.create_text(cx - 55, cy - 50, text="✨", fill=GOLD, font=("Segoe UI Emoji", 14))
            self.create_text(cx + 55, cy - 50, text="🔮", font=("Segoe UI Emoji", 14))

        elif self.mood == "defeated":
            # Worried/surprised eyebrows
            self.create_line(cx - 24, cy - 22, cx - 8, cy - 30, width=3, fill="#1e272e")
            self.create_line(cx + 8, cy - 30, cx + 24, cy - 22, width=3, fill="#1e272e")
            # Wide surprised eyes
            self.create_oval(cx - 24, cy - 22, cx - 8, cy - 4, fill="white", outline="#1e272e", width=2)
            self.create_oval(cx + 8, cy - 22, cx + 24, cy - 4, fill="white", outline="#1e272e", width=2)
            self.create_oval(cx - 18, cy - 15, cx - 14, cy - 10, fill="#1e272e")
            self.create_oval(cx + 14, cy - 15, cx + 18, cy - 10, fill="#1e272e")
            # Open 'O' mouth
            self.create_oval(cx - 8, cy + 2, cx + 8, cy + 14, fill="#1e272e")
            self.create_polygon(cx - 10, cy + 15, cx + 10, cy + 15, cx, cy + 28, fill="#1e272e")
            # Sweat drop
            self.create_text(cx + 42, cy - 30, text="💧", font=("Segoe UI Emoji", 12))


class ModernButton(tk.Button):
    """Custom styled button with smooth hover effects."""

    def __init__(self, master, text, bg_color, hover_color, command=None, text_color=TEXT_WHITE, **kwargs):
        self.default_bg = bg_color
        self.hover_bg = hover_color
        super().__init__(
            master,
            text=text,
            bg=bg_color,
            fg=text_color,
            activebackground=hover_color,
            activeforeground=text_color,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=command,
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _):
        if self["state"] != "disabled":
            self.configure(bg=self.hover_bg)

    def on_leave(self, _):
        if self["state"] != "disabled":
            self.configure(bg=self.default_bg)


class AkinatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Akinator — The Web Genius (Python Edition)")
        self.root.geometry("780x740")
        self.root.minsize(680, 640)
        self.root.configure(bg=BG_DARK)

        # Initialize AI Engine
        self.engine = AkinatorEngine()
        self.current_question: Optional[dict] = None

        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        # Top Header Bar
        header_frame = tk.Frame(self.root, bg=BG_HEADER, pady=12)
        header_frame.pack(fill="x", side="top")

        title_lbl = tk.Label(
            header_frame,
            text="🧞 AKINATOR",
            font=("Segoe UI", 24, "bold"),
            fg=GOLD,
            bg=BG_HEADER
        )
        title_lbl.pack()

        subtitle_lbl = tk.Label(
            header_frame,
            text="Think of a character. I will read your mind!",
            font=("Segoe UI", 11),
            fg=CYAN,
            bg=BG_HEADER
        )
        subtitle_lbl.pack(pady=(2, 0))

        # Main Container
        self.main_container = tk.Frame(self.root, bg=BG_DARK, padx=25, pady=15)
        self.main_container.pack(fill="both", expand=True)

        # Genie & Meter Card
        top_card = tk.Frame(self.main_container, bg=BG_CARD, bd=0, padx=20, pady=15)
        top_card.pack(fill="x", pady=(0, 15))

        # Split into Left (Genie) and Right (Confidence Meter & Info)
        top_card.columnconfigure(0, weight=0)
        top_card.columnconfigure(1, weight=1)

        self.genie = GenieCanvas(top_card, width=190, height=190)
        self.genie.grid(row=0, column=0, rowspan=3, padx=(0, 25))

        # Question counter badge
        self.badge_lbl = tk.Label(
            top_card,
            text="QUESTION #1",
            font=("Segoe UI", 11, "bold"),
            fg=PURPLE_LIGHT,
            bg=BG_CARD
        )
        self.badge_lbl.grid(row=0, column=1, sticky="w", pady=(10, 4))

        # Confidence title & percentage
        meter_info_frame = tk.Frame(top_card, bg=BG_CARD)
        meter_info_frame.grid(row=1, column=1, sticky="ew", pady=(0, 6))

        tk.Label(
            meter_info_frame,
            text="Akinator Confidence:",
            font=("Segoe UI", 11),
            fg=TEXT_MUTED,
            bg=BG_CARD
        ).pack(side="left")

        self.conf_lbl = tk.Label(
            meter_info_frame,
            text="0%",
            font=("Segoe UI", 12, "bold"),
            fg=GOLD,
            bg=BG_CARD
        )
        self.conf_lbl.pack(side="right")

        # Custom canvas progress bar
        self.progress_canvas = tk.Canvas(top_card, height=18, bg="#2d3436", highlightthickness=0)
        self.progress_canvas.grid(row=2, column=1, sticky="ew", pady=(0, 10))

        # Question / Guess Card
        self.card_frame = tk.Frame(self.main_container, bg=BG_CARD, padx=25, pady=25)
        self.card_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.q_text = tk.Label(
            self.card_frame,
            text="Loading questions...",
            font=("Segoe UI", 17, "bold"),
            fg=TEXT_WHITE,
            bg=BG_CARD,
            wraplength=660,
            justify="center"
        )
        self.q_text.pack(expand=True, fill="both", pady=10)

        # Extra description label for Guesses
        self.guess_desc_lbl = tk.Label(
            self.card_frame,
            text="",
            font=("Segoe UI", 11, "italic"),
            fg=CYAN,
            bg=BG_CARD,
            wraplength=600,
            justify="center"
        )

        # Buttons Frame
        self.actions_frame = tk.Frame(self.main_container, bg=BG_DARK)
        self.actions_frame.pack(fill="x", pady=(0, 10))

        # Five Standard Answer Buttons
        self.btn_grid_frame = tk.Frame(self.actions_frame, bg=BG_DARK)
        self.btn_grid_frame.pack(fill="x")
        self.btn_grid_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="btns")

        self.btn_yes = ModernButton(
            self.btn_grid_frame, text="Yes", bg_color=COLOR_YES, hover_color=COLOR_YES_HOVER,
            font=("Segoe UI", 12, "bold"), height=2, command=lambda: self.on_answer(ANSWERS["YES"])
        )
        self.btn_yes.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_probably = ModernButton(
            self.btn_grid_frame, text="Probably", bg_color=COLOR_PROB, hover_color=COLOR_PROB_HOVER,
            font=("Segoe UI", 12, "bold"), height=2, command=lambda: self.on_answer(ANSWERS["PROBABLY"])
        )
        self.btn_probably.grid(row=0, column=1, padx=4, sticky="ew")

        self.btn_dontknow = ModernButton(
            self.btn_grid_frame, text="Don't Know", bg_color=COLOR_DONTKNOW, hover_color=COLOR_DONTKNOW_HOVER,
            font=("Segoe UI", 12, "bold"), height=2, command=lambda: self.on_answer(ANSWERS["DONT_KNOW"])
        )
        self.btn_dontknow.grid(row=0, column=2, padx=4, sticky="ew")

        self.btn_proknot = ModernButton(
            self.btn_grid_frame, text="Probably Not", bg_color=COLOR_PROBNOT, hover_color=COLOR_PROBNOT_HOVER,
            font=("Segoe UI", 12, "bold"), height=2, command=lambda: self.on_answer(ANSWERS["PROBABLY_NOT"])
        )
        self.btn_proknot.grid(row=0, column=3, padx=4, sticky="ew")

        self.btn_no = ModernButton(
            self.btn_grid_frame, text="No", bg_color=COLOR_NO, hover_color=COLOR_NO_HOVER,
            font=("Segoe UI", 12, "bold"), height=2, command=lambda: self.on_answer(ANSWERS["NO"])
        )
        self.btn_no.grid(row=0, column=4, padx=4, sticky="ew")

        # Two Guess Confirmation Buttons (Hidden during questions)
        self.guess_btns_frame = tk.Frame(self.actions_frame, bg=BG_DARK)
        self.guess_btns_frame.columnconfigure((0, 1), weight=1, uniform="guess_btns")

        self.btn_guess_yes = ModernButton(
            self.guess_btns_frame, text="🎉 YES! That's my character!", bg_color=COLOR_YES,
            hover_color=COLOR_YES_HOVER, font=("Segoe UI", 13, "bold"), height=2, command=self.on_guess_correct
        )
        self.btn_guess_yes.grid(row=0, column=0, padx=10, sticky="ew")

        self.btn_guess_no = ModernButton(
            self.guess_btns_frame, text="❌ No, that's wrong!", bg_color=COLOR_NO,
            hover_color=COLOR_NO_HOVER, font=("Segoe UI", 13, "bold"), height=2, command=self.on_guess_wrong
        )
        self.btn_guess_no.grid(row=0, column=1, padx=10, sticky="ew")

        # Bottom Utilities Bar (Undo, Restart, Stats)
        bottom_frame = tk.Frame(self.main_container, bg=BG_DARK)
        bottom_frame.pack(fill="x", side="bottom")

        self.btn_undo = ModernButton(
            bottom_frame, text="↩ Undo Last Answer", bg_color="#2f3542", hover_color="#57606f",
            font=("Segoe UI", 10), padx=14, pady=6, command=self.on_undo
        )
        self.btn_undo.pack(side="left")

        self.btn_restart = ModernButton(
            bottom_frame, text="🔄 Restart", bg_color="#2f3542", hover_color="#57606f",
            font=("Segoe UI", 10), padx=14, pady=6, command=self.start_new_game
        )
        self.btn_restart.pack(side="left", padx=(10, 0))

        self.db_stats_lbl = tk.Label(
            bottom_frame,
            text=f"📚 {len(self.engine.characters)} Characters  •  {len(self.engine.questions)} Questions",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED,
            bg=BG_DARK
        )
        self.db_stats_lbl.pack(side="right")

    def update_meter(self, prob: float):
        """Update confidence display and smooth progress bar."""
        percent = int(prob * 100)
        self.conf_lbl.configure(text=f"{percent}%")

        self.progress_canvas.update_idletasks()
        w = self.progress_canvas.winfo_width()
        h = self.progress_canvas.winfo_height()

        self.progress_canvas.delete("all")
        fill_w = max(0, min(w, int(w * prob)))

        color = COLOR_YES if percent >= 75 else COLOR_PROBNOT if percent >= 45 else CYAN
        self.progress_canvas.create_rectangle(0, 0, fill_w, h, fill=color, outline="")

    def start_new_game(self):
        """Reset game state and show the first question."""
        self.engine.reset()
        self.guess_btns_frame.pack_forget()
        self.btn_grid_frame.pack(fill="x")
        self.guess_desc_lbl.pack_forget()
        self.btn_undo.configure(state="disabled")

        self.genie.set_mood("thinking")
        self.update_meter(0.0)
        self.db_stats_lbl.configure(
            text=f"📚 {len(self.engine.characters)} Characters  •  {len(self.engine.questions)} Questions"
        )
        self.ask_next_question()

    def ask_next_question(self):
        """Pick and display the next optimal question, or trigger guess."""
        top_char, top_prob = self.engine.get_top_candidate()
        self.update_meter(top_prob if top_prob else 0.0)

        # Update Genie mood according to certainty
        if top_prob >= 0.70:
            self.genie.set_mood("confident")
        else:
            self.genie.set_mood("thinking")

        # Check if ready to guess
        if self.engine.should_make_guess():
            self.present_guess(top_char)
            return

        self.current_question = self.engine.get_best_question()
        if not self.current_question:
            # Exhausted questions
            if top_char:
                self.present_guess(top_char)
            else:
                self.show_learning_dialog(None)
            return

        q_num = len(self.engine.asked_questions) + 1
        self.badge_lbl.configure(text=f"QUESTION #{q_num}")
        self.q_text.configure(text=self.current_question["text"])
        self.btn_undo.configure(state="normal" if self.engine.history else "disabled")

    def on_answer(self, value: float):
        """User submitted an answer."""
        if not self.current_question:
            return
        self.engine.submit_answer(self.current_question["id"], value)
        self.ask_next_question()

    def on_undo(self):
        """Revert last answer."""
        if self.engine.undo():
            self.guess_btns_frame.pack_forget()
            self.btn_grid_frame.pack(fill="x")
            self.guess_desc_lbl.pack_forget()
            self.ask_next_question()

    def present_guess(self, character: dict):
        """Display Akinator's guess."""
        self.genie.set_mood("guessing")
        self.update_meter(1.0)
        self.badge_lbl.configure(text="✨ AKINATOR'S GUESS")

        self.q_text.configure(
            text=f"I think you are thinking of...\n\n🔮 {character['name']}!"
        )

        if character.get("description"):
            self.guess_desc_lbl.configure(text=character["description"])
            self.guess_desc_lbl.pack(after=self.q_text, pady=(0, 10))

        # Switch to guess buttons
        self.btn_grid_frame.pack_forget()
        self.guess_btns_frame.pack(fill="x")

    def on_guess_correct(self):
        """Akinator guessed correctly!"""
        self.genie.set_mood("guessing")
        messagebox.showinfo(
            "Akinator Won!",
            "🎉 Brilliant! Akinator guessed right once more!\n\nThanks for playing! Think of another character to challenge him again."
        )
        self.start_new_game()

    def on_guess_wrong(self):
        """Akinator's guess was rejected."""
        self.engine.reject_current_guess()
        rem_char, _ = self.engine.get_top_candidate()
        unasked = [q for q in self.engine.questions if q["id"] not in self.engine.asked_questions]

        if rem_char and unasked and len(self.engine.asked_questions) < 22:
            # Continue asking
            self.guess_btns_frame.pack_forget()
            self.btn_grid_frame.pack(fill="x")
            self.guess_desc_lbl.pack_forget()
            self.genie.set_mood("thinking")
            self.ask_next_question()
        else:
            # Defeat -> Open learning dialog
            top_char, _ = self.engine.get_top_candidate()
            rejected_id = self.engine.ignored_guesses[-1] if self.engine.ignored_guesses else None
            self.show_learning_dialog(rejected_id)

    def show_learning_dialog(self, rejected_char_id: Optional[str]):
        """Open modal dialog allowing the user to teach Akinator the character."""
        self.genie.set_mood("defeated")

        rej_name = "the character I guessed"
        if rejected_char_id and rejected_char_id in self.engine.characters_by_id:
            rej_name = self.engine.characters_by_id[rejected_char_id]["name"]

        learn_win = tk.Toplevel(self.root)
        learn_win.title("Teach Akinator!")
        learn_win.geometry("540x480")
        learn_win.configure(bg=BG_CARD)
        learn_win.grab_set()
        learn_win.transient(self.root)

        tk.Label(
            learn_win,
            text="😲 Bravo! You defeated me!",
            font=("Segoe UI", 16, "bold"),
            fg=GOLD,
            bg=BG_CARD
        ).pack(pady=(18, 4))

        tk.Label(
            learn_win,
            text="Teach me who you were thinking of so I never lose next time!",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED,
            bg=BG_CARD
        ).pack(pady=(0, 15))

        form_frame = tk.Frame(learn_win, bg=BG_CARD, padx=30)
        form_frame.pack(fill="both", expand=True)

        # Character Name
        tk.Label(form_frame, text="Character Name:", font=("Segoe UI", 10, "bold"), fg=TEXT_WHITE, bg=BG_CARD).pack(anchor="w", pady=(5, 2))
        name_entry = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#2d3436", fg=TEXT_WHITE, insertbackground="white")
        name_entry.pack(fill="x", pady=(0, 8))
        name_entry.focus_set()

        # Character Description
        tk.Label(form_frame, text="Short Description (e.g. superhero, actor, scientist):", font=("Segoe UI", 10), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(2, 2))
        desc_entry = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#2d3436", fg=TEXT_WHITE, insertbackground="white")
        desc_entry.pack(fill="x", pady=(0, 8))

        # Distinguishing Question
        tk.Label(form_frame, text=f"Question that differentiates your character from {rej_name}:", font=("Segoe UI", 10, "bold"), fg=CYAN, bg=BG_CARD).pack(anchor="w", pady=(2, 2))
        q_entry = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#2d3436", fg=TEXT_WHITE, insertbackground="white")
        q_entry.pack(fill="x", pady=(0, 8))

        # Answer for new character
        tk.Label(form_frame, text="What is the answer to this question for your character?", font=("Segoe UI", 10), fg=TEXT_WHITE, bg=BG_CARD).pack(anchor="w", pady=(4, 2))

        ans_var = tk.StringVar(value="yes")
        radio_frame = tk.Frame(form_frame, bg=BG_CARD)
        radio_frame.pack(anchor="w", pady=(0, 15))

        tk.Radiobutton(
            radio_frame, text="Yes", variable=ans_var, value="yes",
            bg=BG_CARD, fg=TEXT_WHITE, selectcolor="#2d3436", font=("Segoe UI", 11, "bold"),
            activebackground=BG_CARD, activeforeground=TEXT_WHITE
        ).pack(side="left", padx=(0, 20))

        tk.Radiobutton(
            radio_frame, text="No", variable=ans_var, value="no",
            bg=BG_CARD, fg=TEXT_WHITE, selectcolor="#2d3436", font=("Segoe UI", 11, "bold"),
            activebackground=BG_CARD, activeforeground=TEXT_WHITE
        ).pack(side="left")

        def submit_learning():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            diff_q = q_entry.get().strip()
            ans_val = 1.0 if ans_var.get() == "yes" else 0.0
            rej_ans = 0.0 if ans_val == 1.0 else 1.0

            if not name:
                messagebox.showerror("Error", "Please enter the character's name.", parent=learn_win)
                return
            if not diff_q:
                messagebox.showerror("Error", "Please enter a question to differentiate them.", parent=learn_win)
                return

            if not diff_q.endswith("?"):
                diff_q += "?"

            self.engine.learn_character(
                name=name,
                description=desc,
                new_question_text=diff_q,
                answer_for_new=ans_val,
                answer_for_rejected=rej_ans,
                rejected_char_id=rejected_char_id
            )

            learn_win.destroy()
            messagebox.showinfo(
                "Akinator Learned!",
                f"✨ Fantastic! Akinator has permanently recorded '{name}' into his memory!\nHe will remember this for next time."
            )
            self.start_new_game()

        ModernButton(
            learn_win,
            text="💾 Save & Teach Akinator",
            bg_color=COLOR_YES,
            hover_color=COLOR_YES_HOVER,
            font=("Segoe UI", 12, "bold"),
            pady=10,
            command=submit_learning
        ).pack(fill="x", padx=30, pady=(0, 20))


def run_gui():
    root = tk.Tk()
    app = AkinatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
