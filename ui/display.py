"""Display utilities for game state visualization"""

from typing import Any
from game.constants import MAX_ATTEMPTS
from utils.colours import Fore, Style


class Display:
    """Handles all game display functionality"""
    
    @staticmethod
    def show_game_status(game: Any) -> None:
        """Display current game status (hides bag contents)"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"Attempt {game.attempt_count + 1}/{MAX_ATTEMPTS}")
        
        if game.attempts:
            print("Previous guesses:")
            for i, guess in enumerate(game.attempts, 1):
                colored = game.get_colored_guess(guess)
                print(f"  {i}: {colored}")
        
        # Show only minimal bag info - just the count
        contents = game.letter_bag.get_contents()
        print(f"\nBag Summary:")
        print(f"  {Fore.WHITE}Letters remaining in bag: {contents['count_available']}{Style.RESET_ALL}")
        
        # Show pulled letters if any
        pulled = game.letter_bag.get_pulled_letters()
        if pulled:
            # Only show unique pulled letters, not all pulls
            unique_pulled = sorted(set(pulled))
            print(f"  {Fore.CYAN}Letters you've pulled: {' '.join(unique_pulled)}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    @staticmethod
    def show_final_results(game: Any) -> None:
        """Display final game results"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}=== Game Over ==={Style.RESET_ALL}")
        print(f"Secret word: {game.secret_word.upper()}")
        print(f"Attempts used: {game.attempt_count}/{MAX_ATTEMPTS}")
        
        print("\nYour guesses:")
        for i, guess in enumerate(game.attempts, start=1):
            colored = game.get_colored_guess(guess)
            print(f"  {i}: {colored}")

        if game.has_won:
            print(f"\n{Fore.GREEN}🎉 You Won! Congratulations! 🎉{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}You Lost. Better luck next time!{Style.RESET_ALL}")