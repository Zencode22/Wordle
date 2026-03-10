"""Core Wordle game logic with FSM implementation"""

import random
from typing import List, Dict, Optional

from game.constants import MAX_ATTEMPTS, WORD_LENGTH, generate_secret_word
from game.states import State
from models.letter_bag import LetterBag
from models.keyboard import Keyboard
from ui.display import Display
from utils.colours import Fore, Style


class Wordle:
    """Main Wordle game class implementing the FSM"""
    
    def __init__(self, secret_word: Optional[str] = None):
        self.secret_word: str = secret_word or generate_secret_word()
        self.attempt_count: int = 0
        self.has_won: bool = False
        self.attempts: List[str] = []
        self.letter_bag = LetterBag()
        self.keyboard = Keyboard()
        self.display = Display()
        
    def play_round(self) -> None:
        """Run the FSM that drives a single round of Wordle"""
        state = State.WORD_ENTRY
        current_guess = ""

        while True:
            if state == State.WORD_ENTRY:
                # Check if game is over before allowing another guess
                if self.is_game_over():
                    state = State.DISPLAY
                    continue
                    
                self.display.show_game_status(self)
                self.keyboard.display()
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
                print("\n--- Scoring Guess ---")
                self.keyboard.display()
                state = State.PROCESS_LETTERS

            elif state == State.PROCESS_LETTERS:
                self._process_guess_letters(current_guess)
                state = State.IS_WINNER

            elif state == State.IS_WINNER:
                if self._is_winner_state():
                    state = State.DISPLAY
                else:
                    state = State.REVIEW

            elif state == State.REVIEW:
                self._review_state(current_guess)
                # Check if game is over after review
                if self.is_game_over():
                    state = State.DISPLAY
                else:
                    state = State.WORD_ENTRY

            elif state == State.DISPLAY:
                self._display_state()
                return

    def _word_entry_state(self) -> Optional[str]:
        """Prompt for a 5‑letter guess."""
        while True:
            print("\nOptions:")
            print("  - Enter a 5-letter guess")
            print("  - Type 'quit' to exit round")
            
            user_input = input("\nYour choice: ").strip().lower()
            
            if user_input == "quit":
                print("Round aborted by player.")
                return None
            
            if len(user_input) != WORD_LENGTH or not user_input.isalpha():
                print(f"Invalid input – please enter exactly {WORD_LENGTH} letters.")
                continue
            
            # Check if guess has duplicate letters
            if len(set(user_input)) != WORD_LENGTH:
                print(f"Your guess has duplicate letters. The secret word has all unique letters!")
                continue
            
            return user_input

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
        """Record the guess and update keyboard."""
        self.attempts.append(guess)
        self.attempt_count += 1
        self.keyboard.update_from_guess(guess, self.secret_word)

    def _process_guess_letters(self, guess: str) -> None:
        """Process each letter in the guess and update bag accordingly"""
        # Determine status of each letter
        letter_status = self._get_letter_status(guess)
        
        # Process each unique letter based on its highest status
        processed = set()
        for ch in guess:
            if ch in processed:
                continue
            
            status = letter_status[ch]
            
            if status == "GREEN":
                self.letter_bag.lock_green_letter(ch)
            elif status == "YELLOW":
                if ch.upper() not in self.letter_bag.green_letters:
                    self.letter_bag.return_yellow_letter(ch)
            else:  # RED
                if (ch.upper() not in self.letter_bag.green_letters and 
                    ch.upper() not in self.letter_bag.yellow_letters):
                    self.letter_bag.remove_red_letter(ch)
            
            processed.add(ch)

    def _get_letter_status(self, guess: str) -> Dict[str, str]:
        """Get the status of each letter in the guess"""
        letter_status = {}
        for idx, ch in enumerate(guess):
            if ch == self.secret_word[idx]:
                letter_status[ch] = "GREEN"
            elif ch in self.secret_word:
                # Only set to YELLOW if not already GREEN
                if letter_status.get(ch) != "GREEN":
                    letter_status[ch] = "YELLOW"
            else:
                # Only set to RED if not already GREEN or YELLOW
                if ch not in letter_status:
                    letter_status[ch] = "RED"
        return letter_status

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

        print(f"\n{Fore.CYAN}--- Review ---{Style.RESET_ALL}")
        if present:
            print(f"Letters in the word (any position): {', '.join(present)}")
        else:
            print("No new letters from your guess are in the secret word.")

        if correct_pos:
            print(f"Letters in the correct position: {', '.join(correct_pos)}")
        else:
            print("No letters are in the correct position.")
        print(f"{Fore.CYAN}----------------{Style.RESET_ALL}\n")

    def _display_state(self) -> None:
        """Show all attempts, attempt count, and final outcome."""
        self.display.show_final_results(self)
        self.letter_bag.display_status()
        self.keyboard.display()
        
        # Add explicit message about running out of attempts
        if self.attempt_count >= MAX_ATTEMPTS and not self.has_won:
            print(f"\n{Fore.RED}You've used all {MAX_ATTEMPTS} attempts!{Style.RESET_ALL}")
        
        input("\nPress Enter to return to the main menu...")

    def is_game_over(self) -> bool:
        """True if win or max attempts reached."""
        return self.has_won or self.attempt_count >= MAX_ATTEMPTS

    def get_colored_guess(self, guess: str) -> str:
        """Return a colored version of a guess"""
        colored = ""
        for idx, ch in enumerate(guess):
            if ch == self.secret_word[idx]:
                colored += f"{Fore.GREEN}{ch.upper()}{Style.RESET_ALL}"
            elif ch in self.secret_word:
                colored += f"{Fore.YELLOW}{ch.upper()}{Style.RESET_ALL}"
            else:
                colored += f"{Fore.RED}{ch.upper()}{Style.RESET_ALL}"
        return colored