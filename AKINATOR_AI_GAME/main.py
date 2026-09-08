"""
Akinator Launcher
Run default desktop GUI or pass --cli for terminal mode.
Usage:
    python main.py         # Launches the modern desktop GUI
    python main.py --cli   # Launches the terminal CLI version
"""

import sys

def main():
    if "--cli" in sys.argv or "-c" in sys.argv:
        from cli import run_cli
        run_cli()
    else:
        try:
            from gui import run_gui
            run_gui()
        except Exception as e:
            print(f"Failed to launch GUI ({e}). Falling back to Terminal CLI...\n")
            from cli import run_cli
            run_cli()

if __name__ == "__main__":
    main()
