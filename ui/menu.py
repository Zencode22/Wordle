"""Main menu and navigation for the Wordle game"""

from utils.colours import Fore, Style
from game.wordle import Wordle


class MainMenu:
    """Handles main menu display and navigation"""
    
    @staticmethod
    def show() -> None:
        """Display the main menu and handle user choices"""
        while True:
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}=== WORDLE WITH DYNAMIC LETTER BAG ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print("\n1. Start New Game")
            print("2. How to Play")
            print("3. Quit")
            
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == "1":
                game = Wordle()
                game.play_round()
            elif choice == "2":
                MainMenu._show_instructions()
            elif choice == "3":
                print(f"\n{Fore.GREEN}Thanks for playing! Goodbye!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")

    @staticmethod
    def _show_instructions() -> None:
        """Display game instructions"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print("HOW TO PLAY")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print("""
1. Guess the 5-letter word in 6 attempts
2. After each guess, the color of the tiles will change:
   - 🟩 GREEN: Letter is correct and in the right position
   - 🟨 YELLOW: Letter is in the word but wrong position
   - 🟥 RED: Letter is not in the word

3. DYNAMIC LETTER BAG SYSTEM (HIDDEN):
   - The bag starts with one of each letter (A-Z), but you CAN'T see what's inside!
   - 🟩 GREEN letters: Locked in place and removed from bag permanently
   - 🟨 YELLOW letters: Returned to the bag (can be pulled again later)
   - 🟥 RED letters: Removed from the game permanently
   
4. STRATEGY:
   - Pull letters from the bag to discover what's inside
   - Each pull reveals if the letter is in the secret word
   - Yellow letters can be reused - try them in different positions
   - Red letters are gone forever - avoid guessing them!
   - Green letters are locked - focus on finding the remaining letters
   - The bag is a mystery - you only know what you've pulled!

5. Commands during gameplay:
   - Type your 5-letter guess to play
   - Type 'bag' to access the letter bag menu (pull letters)
   - Type 'status' to see what you've learned so far
   - Type 'quit' to exit the current round
        """)
        input("\nPress Enter to return to the main menu...")