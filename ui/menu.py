"""Main menu system for the Wordle game"""

import sys
from utils.colours import Fore, Style
from game.wordle import Wordle


class MainMenu:
    """Handles the main menu and user interaction"""
    
    @staticmethod
    def show() -> None:
        """Display the main menu and handle user choices"""
        while True:
            MainMenu._display_header()
            MainMenu._display_options()
            
            choice = input("\nSelect an option (1‑3): ").strip()

            if choice == "1":
                game = Wordle()
                game.play_round()
            elif choice == "2":
                MainMenu._show_instructions()
            elif choice == "3":
                MainMenu._exit_game()
            else:
                print(f"{Fore.RED}Invalid selection – please choose 1, 2, or 3.{Style.RESET_ALL}")

    @staticmethod
    def _display_header() -> None:
        """Display the game header"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}=== WORDLE GAME with DYNAMIC LETTER BAG ==={Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    @staticmethod
    def _display_options() -> None:
        """Display menu options"""
        print("1) Play a round of Wordle")
        print("2) View game instructions")
        print("3) Leave")

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

3. DYNAMIC LETTER BAG SYSTEM:
   - The bag starts with one of each letter (A-Z)
   - 🟩 GREEN letters: Locked in place and removed from bag permanently
   - 🟨 YELLOW letters: Returned to the bag (can be pulled again)
   - 🟥 RED letters: Removed from the game permanently
   
4. STRATEGY:
   - Pull letters from the bag to get hints
   - Yellow letters can be reused in different positions
   - Red letters are gone forever - avoid guessing them!
   - Green letters are locked - focus on finding the remaining letters

5. Commands:
   - Type your 5-letter guess to play
   - Type 'bag' to access the letter bag menu
   - Type 'status' to view bag status
   - Type 'quit' to exit the current round
        """)
        input("\nPress Enter to return to the main menu...")

    @staticmethod
    def _exit_game() -> None:
        """Exit the game gracefully"""
        print(f"\n{Fore.GREEN}Thanks for playing – come back another time!{Style.RESET_ALL}")
        sys.exit(0)