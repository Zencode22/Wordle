#!/usr/bin/env python3
"""
Wordle Finite State Machine (FSM) – console version

Author: Connor Lonergan
Purpose: Demonstrate state‑machine design without Boolean state flags.
"""

import enum
import random
import sys
from typing import List


# ----------------------------------------------------------------------
# Helper: a tiny built‑in word list (feel free to replace with a larger list)
# ----------------------------------------------------------------------
WORD_LIST = [
    "apple", "brave", "cigar", "delta", "eagle",
    "flame", "grape", "honey", "index", "joker",
    "karma", "lemon", "mango", "nerve", "ocean",
    "piano", "queen", "raven", "spice", "tiger",
    "ultra", "vivid", "waltz", "xenon", "yacht", "zebra"
]


# ----------------------------------------------------------------------
# FSM State definition
# ----------------------------------------------------------------------
class State(enum.Enum):
    WORD_ENTRY = enum.auto()
    CONFIRM = enum.auto()
    SCORE = enum.auto()
    IS_WINNER = enum.auto()
    REVIEW = enum.auto()
    CONFIRM_AFTER_REVIEW = enum.auto()
    DISPLAY = enum.auto()


# ----------------------------------------------------------------------
# Core Wordle class
# ----------------------------------------------------------------------
class Wordle:
    MAX_ATTEMPTS = 6

    def __init__(self, secret_word: str | None = None):
        self.secret_word: str = secret_word or random.choice(WORD_LIST)
        self.attempt_count: int = 0
        self.has_won: bool = False
        self.attempts: List[str] = []

    # --------------------------------------------------------------
    # Public API called from the main loop
    # --------------------------------------------------------------
    def play_round(self) -> None:
        """Run the FSM that drives a single round of Wordle."""
        state = State.WORD_ENTRY
        current_guess = ""

        while True:
            if state == State.WORD_ENTRY:
                current_guess = self._word_entry_state()
                if current_guess is None:          # user chose to quit
                    return
                state = State.CONFIRM

            elif state == State.CONFIRM:
                if self._confirm_state(current_guess):
                    state = State.SCORE
                else:
                    state = State.WORD_ENTRY

            elif state == State.SCORE:
                self._score_state(current_guess)
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
                # No extra confirmation needed; just loop back
                state = State.WORD_ENTRY

            elif state == State.DISPLAY:
                self._display_state()
                return

    # --------------------------------------------------------------
    # FSM state implementations
    # --------------------------------------------------------------
    def _word_entry_state(self) -> str | None:
        """Prompt for a 5‑letter guess. Return None if the player quits."""
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
        """Record the guess and increment the attempt counter."""
        self.attempts.append(guess)
        self.attempt_count += 1

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

        # Remove duplicates for cleaner output
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
            print(f"  {i}: {g}")

        if self.has_won:
            print("\nYou Won!")
        else:
            print("\nYou Lost.")
        input("\nPress Enter to return to the main menu...")

    # --------------------------------------------------------------
    # Convenience method for external callers (not part of FSM)
    # --------------------------------------------------------------
    def is_game_over(self) -> bool:
        """True if win or max attempts reached."""
        return self.has_won or self.attempt_count >= self.MAX_ATTEMPTS


# ----------------------------------------------------------------------
# Main menu loop
# ----------------------------------------------------------------------
def main_menu() -> None:
    while True:
        print("\n=== Wordle FSM ===")
        print("1) Play a round of Wordle")
        print("2) Leave")
        choice = input("Select an option (1‑2): ").strip()

        if choice == "1":
            game = Wordle()
            game.play_round()
        elif choice == "2":
            print("\nThanks for Playing and come back another time!")
            sys.exit(0)
        else:
            print("Invalid selection – please choose 1 or 2.")


if __name__ == "__main__":
    main_menu()