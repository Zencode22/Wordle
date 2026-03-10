"""Core Wordle game logic with FSM implementation"""

import random
from typing import List, Dict, Optional

from game.constants import WORD_LIST, MAX_ATTEMPTS, WORD_LENGTH, COLOUR_HIERARCHY
from game.states import State
from models.letter_bag import LetterBag
from models.keyboard import Keyboard
from ui.display import Display
from utils.colours import Fore, Style


class Wordle:
    """Main Wordle game class implementing the FSM"""
    
    def __init__(self, secret_word: Optional[str] = None):
        self.secret_word: str = secret_word or random.choice(WORD_LIST)
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
                state = State.BAG_MENU

            elif state == State.BAG_MENU:
                self._bag_menu_state()
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
            print("  - Type 'bag' to access the letter bag")
            print("  - Type 'status' to view bag status")
            print("  - Type 'quit' to exit round")
            
            user_input = input("\nYour choice: ").strip().lower()
            
            if user_input == "quit":
                print("Round aborted by player.")
                return None
            elif user_input == "bag":
                self._bag_menu_state()
                continue
            elif user_input == "status":
                self.letter_bag.display_status()
                continue
            
            if len(user_input) != WORD_LENGTH or not user_input.isalpha():
                print(f"Invalid input – please enter exactly {WORD_LENGTH} letters.")
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
        print(f"\n{Fore.MAGENTA}--- Processing Letter Status ---{Style.RESET_ALL}")
        
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
        
        print(f"{Fore.MAGENTA}--- Processing Complete ---{Style.RESET_ALL}")
        self.letter_bag.display_status()

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

    def _bag_menu_state(self) -> None:
        """Handle letter bag interactions"""
        while not self.is_game_over():
            print(f"\n{Fore.CYAN}=== LETTER BAG MENU ==={Style.RESET_ALL}")
            print("1) Pull a letter from the bag")
            print("2) View detailed bag status")
            print("3) View available hints")
            print("4) Return to game")
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == "1":
                if not self.letter_bag.can_pull():
                    print(f"{Fore.RED}No letters available to pull!{Style.RESET_ALL}")
                else:
                    letter = self.letter_bag.pull_letter()
                    if letter:
                        print(f"\n{Fore.GREEN}You pulled: {letter}{Style.RESET_ALL}")
                        self._analyze_pulled_letter(letter.lower())
                    else:
                        print(f"{Fore.RED}Failed to pull a letter.{Style.RESET_ALL}")
            
            elif choice == "2":
                self.letter_bag.display_status()
            
            elif choice == "3":
                self._display_hints()
            
            elif choice == "4":
                break
            
            else:
                print("Invalid selection – please choose 1-4.")

    def _analyze_pulled_letter(self, letter: str) -> None:
        """Analyze a pulled letter and provide hints"""
        print(f"\n{Fore.CYAN}=== Letter Analysis ==={Style.RESET_ALL}")
        
        if letter in self.secret_word:
            print(f"{Fore.GREEN}Good news! '{letter.upper()}' IS in the secret word!{Style.RESET_ALL}")
            
            positions = [i+1 for i, ch in enumerate(self.secret_word) if ch == letter]
            if len(positions) == 1:
                print(f"It appears in position {positions[0]}")
            else:
                print(f"It appears in positions: {', '.join(map(str, positions))}")
        else:
            print(f"{Fore.RED}Sorry, '{letter.upper()}' is NOT in the secret word.{Style.RESET_ALL}")
            print("This letter will be removed permanently if you guess it.")
        
        print(f"{Fore.CYAN}===================={Style.RESET_ALL}")

    def _display_hints(self) -> None:
        """Show available hint information"""
        contents = self.letter_bag.get_contents()
        
        print(f"\n{Fore.CYAN}=== HINT SUMMARY ==={Style.RESET_ALL}")
        
        if contents["green"]:
            print(f"{Fore.GREEN}✅ Locked correct letters: {' '.join(contents['green'])}{Style.RESET_ALL}")
        
        if contents["yellow"]:
            print(f"{Fore.YELLOW}🟡 Letters in word (wrong position): {' '.join(contents['yellow'])}{Style.RESET_ALL}")
        
        if contents["removed"]:
            print(f"{Fore.RED}❌ Letters not in word: {' '.join(contents['removed'])}{Style.RESET_ALL}")
        
        if contents["available"]:
            print(f"{Fore.WHITE}📦 Available to pull: {' '.join(contents['available'])}{Style.RESET_ALL}")
        else:
            print(f"{Fore.WHITE}📦 No letters available to pull{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}==================={Style.RESET_ALL}")

    def _display_state(self) -> None:
        """Show all attempts, attempt count, and final outcome."""
        self.display.show_final_results(self)
        self.letter_bag.display_status()
        self.keyboard.display()
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