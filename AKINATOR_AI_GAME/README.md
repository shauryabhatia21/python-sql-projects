# 🧞 Akinator — The Web Genius (Python Edition)

An intelligent, self-learning clone of the famous Akinator (20 Questions / Guess the Character) game built in Python.

---

## 🌟 Features

1. **Intelligent Decision Engine (`engine.py`)**:
   - Uses **Information Entropy / Variance** to select questions that best split remaining candidates 50/50.
   - **Bayesian Likelihood Scoring** with soft decay so uncertain answers don't prematurely eliminate characters.
   - **5-Point Response System**: *Yes (1.0)*, *Probably (0.75)*, *Don't Know (0.5)*, *Probably Not (0.25)*, *No (0.0)*.
   - Full **Undo** history support to take back an accidental click or answer.

2. **Self-Learning AI**:
   - If Akinator is stumped or guesses wrong, it admits defeat and asks you:
     - Who were you thinking of?
     - What question differentiates your character from Akinator's guess?
     - What would the answer be for your character?
   - Permanently saves the new character, question, and answers to `akinator_db.json` so Akinator gets smarter after every session!

3. **Modern Desktop GUI (`gui.py`)**:
   - Built with **Tkinter**.
   - Custom dynamic **Genie character canvas** with responsive mood animations (*Thinking 🧞*, *Confident 🔮*, *Guessing 🧞‍♂️*, *Surprised / Defeated 😲*).
   - Live confidence progress meter and question counter.
   - 5 color-coded response buttons with hover transitions.
   - Interactive modals for guessing and teaching new characters.

4. **Terminal CLI (`cli.py`)**:
   - Fast, ANSI-colored terminal game with ASCII Genie banner, meter bar, and keyboard shortcuts.

---

## 🚀 How to Run

Navigate to the Akinator folder:
```powershell
cd "c:\py Programs\AKINATOR"
```

### 1. Launch Modern Desktop GUI:
```powershell
python main.py
```
*(or double-click `main.py`)*

### 2. Launch Terminal CLI Version:
```powershell
python main.py --cli
```

---

## 📂 Project Structure

- `main.py` — Entry point launcher (defaults to GUI, accepts `--cli`).
- `gui.py` — Modern Tkinter graphical desktop application.
- `cli.py` — Colored interactive command-line interface.
- `engine.py` — Core AI logic (entropy question picker, Bayesian probability scoring, history, and learning).
- `akinator_db.json` — Knowledge base containing 30+ characters and 35+ questions.
- `test_engine.py` — Automated test suite to verify question selection, character guessing, and database persistence.
