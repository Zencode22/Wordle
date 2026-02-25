#!/usr/bin/env python3
"""
Wordle Finite State Machine (FSM) – console version with on‑screen keyboard
"""

import enum
import random
import sys
from typing import List, Dict

# --------------------------------------------------------------
# Colour handling (cross‑platform)
# --------------------------------------------------------------
# Attempt to import colorama which enables ANSI code processing on
# Windows. If the module isn't installed we will try to install it
# automatically; failing that we warn the user and degrade gracefully.

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # We couldn't import colorama. It's nice to have, but not strictly
    # required: the only reason is to enable ANSI escape processing on
    # Windows consoles. We can attempt to turn that on manually and then
    # fallback to raw ANSI codes for the colour constants.
    if sys.platform.startswith("win"):
        try:
            import ctypes, os
            kernel32 = ctypes.windll.kernel32
            h = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(h, ctypes.byref(mode)):
                # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                new_mode = mode.value | 0x0004
                kernel32.SetConsoleMode(h, new_mode)
            # a dummy os.system call sometimes forces the console to
            # respect the updated mode on Python <3.9
            os.system("")
        except Exception:
            pass

    # Define simple ANSI values; they may or may not be interpreted but at
    # least the strings aren't empty.
    class _Fore:
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        WHITE = '\033[37m'
    class _Style:
        BRIGHT = '\033[1m'
        NORMAL = '\033[0m'
        RESET_ALL = '\033[0m'
    Fore, Style = _Fore(), _Style()

    print("Warning: 'colorama' module not found. Colours may not display\n"
          "correctly on this platform. You can install it with:\n"
          "    pip install colorama")

# --------------------------------------------------------------
# Tiny built‑in word list
# --------------------------------------------------------------
WORD_LIST = [
    "apple", "brave", "cigar", "delta", "eagle",
    "flame", "grape", "honey", "index", "joker",
    "karma", "lemon", "mango", "nerve", "ocean",
    "piano", "queen", "raven", "spice", "tiger",
    "ultra", "vivid", "waltz", "xenon", "yacht", "zebra"
]

# --------------------------------------------------------------
# FSM State definition
# --------------------------------------------------------------
class State(enum.Enum):
    WORD_ENTRY = enum.auto()
    CONFIRM = enum.auto()
    SCORE = enum.auto()
    IS_WINNER = enum.auto()
    REVIEW = enum.auto()
    CONFIRM_AFTER_REVIEW = enum.auto()
    DISPLAY = enum.auto()


# --------------------------------------------------------------
# Core Wordle class
# --------------------------------------------------------------
class Wordle:
    MAX_ATTEMPTS = 6
    _KB_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

    def __init__(self, secret_word: str | None = None):
        self.secret_word: str = secret_word or random.choice(WORD_LIST)
        self.attempt_count: int = 0
        self.has_won: bool = False
        self.attempts: List[str] = []
        self._key_status: Dict[str, str] = {ch: "WHITE" for ch in "abcdefghijklmnopqrstuvwxyz"}

    def play_round(self) -> None:
        """Run the FSM that drives a single round of Wordle."""
        state = State.WORD_ENTRY
        current_guess = ""

        while True:
            if state == State.WORD_ENTRY:
                self._display_keyboard()
                current_guess = self._word_entry_state()
                if current_guess is None:
                    return
                state = State.CONFIRM

            elif state == State.CONFIRM:
                if self._confirm_state(current_guess):
                    state = State.SCORE
                else:
                    state = State.WORD_ENTRY

            elif state == State.SCORE:
                self._score_state(current_guess)
                # Show updated keyboard immediately after scoring
                print("\n--- Updated Keyboard ---")
                self._display_keyboard()
                state = State.IS_WINNER

            elif state == State.IS_WINNER:
                if self._is_winner_state():
                    state = State.DISPLAY
                else:
                    state = State.REVIEW

            elif state == State.REVIEW:
                self._review_state(current_guess)
                state = State.CONFIRM_AFTER_REVIEW

            elif state == State.CONFIRM_AFTER_REVIEW:
                if self.is_game_over():
                    state = State.DISPLAY
                else:
                    state = State.WORD_ENTRY

            elif state == State.DISPLAY:
                self._display_state()
                return

    def _word_entry_state(self) -> str | None:
        """Prompt for a 5‑letter guess."""
        while True:
            guess = input("\nEnter a 5‑letter guess (or type 'quit' to exit round): ").strip().lower()
            if guess == "quit":
                print("Round aborted by player.")
                return None
            if len(guess) != 5 or not guess.isalpha():
                print("Invalid input – please enter exactly five letters.")
                continue
            return guess

    def _confirm_state(self, guess: str) -> bool:
        """Ask the player to confirm the entered guess."""
        while True:
            resp = input(f"You entered '{guess}'. Proceed? (y/n): ").strip().lower()
            if resp in {"y", "yes"}:
                return True
            if resp in {"n", "no"}:
                return False
            print("Please answer with 'y' or 'n'.")

    def _score_state(self, guess: str) -> None:
        """Record the guess, increment the attempt counter, and update keyboard."""
        self.attempts.append(guess)
        self.attempt_count += 1
        self._update_key_status(guess)

    def _is_winner_state(self) -> bool:
        """Check whether the latest guess matches the secret word."""
        if self.attempts[-1] == self.secret_word:
            self.has_won = True
        return self.has_won

    def _review_state(self, guess: str) -> None:
        """Provide feedback about present letters and correct positions."""
        present = []
        correct_pos = []

        for idx, ch in enumerate(guess):
            if ch == self.secret_word[idx]:
                correct_pos.append(ch)
            elif ch in self.secret_word:
                present.append(ch)

        present = sorted(set(present))
        correct_pos = sorted(set(correct_pos))

        print("\n--- Review ---")
        if present:
            print(f"Letters in the word (any position): {', '.join(present)}")
        else:
            print("No letters from your guess are in the secret word.")

        if correct_pos:
            print(f"Letters in the correct position: {', '.join(correct_pos)}")
        else:
            print("No letters are in the correct position.")
        print("----------------\n")

    def _display_state(self) -> None:
        """Show all attempts, attempt count, and final outcome."""
        print("\n=== Game Over ===")
        print(f"Secret word: {self.secret_word}")
        print(f"Attempts used: {self.attempt_count}/{self.MAX_ATTEMPTS}")
        print("Your guesses:")
        for i, g in enumerate(self.attempts, start=1):
            colored_guess = ""
            for idx, ch in enumerate(g):
                if ch == self.secret_word[idx]:
                    colored_guess += f"{Fore.GREEN}{ch.upper()}{Style.RESET_ALL}"
                elif ch in self.secret_word:
                    colored_guess += f"{Fore.YELLOW}{ch.upper()}{Style.RESET_ALL}"
                else:
                    colored_guess += f"{Fore.RED}{ch.upper()}{Style.RESET_ALL}"
            print(f"  {i}: {colored_guess}")

        # Show final keyboard
        print("\nFinal Keyboard Status:")
        self._display_keyboard()

        if self.has_won:
            print(f"\n{Fore.GREEN}You Won!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}You Lost.{Style.RESET_ALL}")
        input("\nPress Enter to return to the main menu...")

    def is_game_over(self) -> bool:
        """True if win or max attempts reached."""
        return self.has_won or self.attempt_count >= self.MAX_ATTEMPTS

    def _update_key_status(self, guess: str) -> None:
        """
        Update the stored colour for each letter based on the most recent guess.
        The hierarchy is: GREEN > YELLOW > RED > WHITE.
        """
        for idx, ch in enumerate(guess):
            if ch == self.secret_word[idx]:
                new_colour = "GREEN"
            elif ch in self.secret_word:
                new_colour = "YELLOW"
            else:
                new_colour = "RED"

            current = self._key_status[ch]
            hierarchy = {"WHITE": 0, "RED": 1, "YELLOW": 2, "GREEN": 3}
            if hierarchy[new_colour] > hierarchy[current]:
                self._key_status[ch] = new_colour

    def _display_keyboard(self) -> None:
        """Print the QWERTY keyboard with current colour coding."""
        colour_map = {
            "WHITE": Fore.WHITE + Style.BRIGHT,
            "RED":   Fore.RED + Style.BRIGHT,
            "YELLOW": Fore.YELLOW + Style.BRIGHT,
            "GREEN": Fore.GREEN + Style.BRIGHT,
        }

        print("\n" + "="*40)
        print("KEYBOARD STATUS:")
        print("="*40)
        for row in self._KB_ROWS:
            line = ""
            for ch in row:
                col = colour_map[self._key_status[ch]]
                line += f"{col}{ch.upper()}{Style.RESET_ALL} "
            print(f"  {line.rstrip()}")
        print("="*40)


# --------------------------------------------------------------
# Main menu loop
# --------------------------------------------------------------
def main_menu() -> None:
    while True:
        print("\n" + "="*40)
        print("=== Wordle FSM ===")
        print("="*40)
        print("1) Play a round of Wordle")
        print("2) Leave")
        choice = input("Select an option (1‑2): ").strip()

        if choice == "1":
            game = Wordle()
            game.play_round()
        elif choice == "2":
            print("\nThanks for playing – come back another time!")
            sys.exit(0)
        else:
            print("Invalid selection – please choose 1 or 2.")


if __name__ == "__main__":
    main_menu()