"""Keyboard model for tracking letter statuses"""

from typing import Dict
from game.constants import KEYBOARD_ROWS, COLOUR_HIERARCHY
from utils.colours import Fore, Style


class Keyboard:
    """Manages the on-screen keyboard and letter statuses"""
    
    def __init__(self):
        self._key_status: Dict[str, str] = {
            ch: "WHITE" for ch in "abcdefghijklmnopqrstuvwxyz"
        }
        self._colour_map = {
            "WHITE": Fore.WHITE + Style.BRIGHT,
            "RED": Fore.RED + Style.BRIGHT,
            "YELLOW": Fore.YELLOW + Style.BRIGHT,
            "GREEN": Fore.GREEN + Style.BRIGHT,
        }
    
    def update_from_guess(self, guess: str, secret_word: str) -> None:
        """Update keyboard status based on a guess"""
        for idx, ch in enumerate(guess):
            if ch == secret_word[idx]:
                new_colour = "GREEN"
            elif ch in secret_word:
                new_colour = "YELLOW"
            else:
                new_colour = "RED"
            
            self._update_letter_status(ch, new_colour)
    
    def _update_letter_status(self, letter: str, new_colour: str) -> None:
        """Update a single letter's status with hierarchy"""
        current = self._key_status[letter]
        if COLOUR_HIERARCHY[new_colour] > COLOUR_HIERARCHY[current]:
            self._key_status[letter] = new_colour
    
    def display(self) -> None:
        """Print the QWERTY keyboard with current colour coding"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print("KEYBOARD STATUS (Green=Correct, Yellow=Wrong position, Red=Not in word)")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        for row in KEYBOARD_ROWS:
            line = ""
            for ch in row:
                col = self._colour_map[self._key_status[ch]]
                line += f"{col}{ch.upper()}{Style.RESET_ALL} "
            print(f"  {line.rstrip()}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    def get_status(self, letter: str) -> str:
        """Get the status of a specific letter"""
        return self._key_status.get(letter, "WHITE")