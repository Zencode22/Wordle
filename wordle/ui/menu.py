"""Main menu and navigation for the Wordle game"""

from utils.colours import Fore, Style, clear_screen
from game.wordle import Wordle


class MainMenu:
    """Handles main menu display and navigation"""
    
    @staticmethod
    def show() -> None:
        """Display the main menu and handle user choices"""
        while True:
            clear_screen()
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}=== WORDLE WITH DYNAMIC LETTER BAG ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print("\n1. Start New Game")
            print("2. How to Play")
            print("3. Quit")
            
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == "1":
                clear_screen()
                game = Wordle()
                game.play_round()
            elif choice == "2":
                clear_screen()
                MainMenu._show_instructions()
            elif choice == "3":
                clear_screen()
                print(f"\n{Fore.GREEN}Thanks for playing! Goodbye!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")

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
        """)
        input("\nPress Enter to return to the main menu...")