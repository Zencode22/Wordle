"""Letter Bag model for managing game letters"""

import random
from typing import List, Set, Dict, Optional
from utils.colours import Fore, Style


class LetterBag:
    """A bag containing letters that are dynamically managed based on game state"""
    
    def __init__(self):
        self.available_letters: List[str] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.permanently_removed: Set[str] = set()  # Red letters - gone forever
        self.green_letters: Set[str] = set()        # Green letters - removed from bag
        self.yellow_letters: Set[str] = set()       # Yellow letters - in bag but marked
        self.pulled_history: List[str] = []         # Track all pulls for history
        
        random.shuffle(self.available_letters)
    
    def pull_letter(self) -> Optional[str]:
        """Pull a random letter from available letters only"""
        available = self._get_available_pullable_letters()
        
        if not available:
            return None
            
        letter = random.choice(available)
        self.available_letters.remove(letter)
        self.pulled_history.append(letter)
        return letter
    
    def _get_available_pullable_letters(self) -> List[str]:
        """Get letters that are currently available to pull"""
        return [l for l in self.available_letters 
                if l not in self.green_letters 
                and l not in self.permanently_removed]
    
    def return_yellow_letter(self, letter: str) -> None:
        """Return a yellow letter to the available pool"""
        letter = letter.upper()
        if letter not in self.available_letters and letter not in self.green_letters:
            self.available_letters.append(letter)
            self.yellow_letters.add(letter)
            random.shuffle(self.available_letters)
            print(f"{Fore.YELLOW}Letter {letter} returned to bag (yellow status){Style.RESET_ALL}")
    
    def remove_red_letter(self, letter: str) -> None:
        """Permanently remove a red letter from the game"""
        letter = letter.upper()
        self.permanently_removed.add(letter)
        if letter in self.available_letters:
            self.available_letters.remove(letter)
        if letter in self.yellow_letters:
            self.yellow_letters.remove(letter)
        print(f"{Fore.RED}Letter {letter} removed permanently (red status){Style.RESET_ALL}")
    
    def lock_green_letter(self, letter: str) -> None:
        """Lock a green letter (remove from bag, keep on board)"""
        letter = letter.upper()
        self.green_letters.add(letter)
        if letter in self.available_letters:
            self.available_letters.remove(letter)
        if letter in self.yellow_letters:
            self.yellow_letters.remove(letter)
        print(f"{Fore.GREEN}Letter {letter} locked in place (green status){Style.RESET_ALL}")
    
    def get_contents(self) -> Dict[str, List[str]]:
        """Get current bag status for display"""
        available = self._get_available_pullable_letters()
        
        return {
            "available": sorted(available),
            "yellow": sorted(self.yellow_letters),
            "green": sorted(self.green_letters),
            "removed": sorted(self.permanently_removed)
        }
    
    def display_status(self) -> None:
        """Show bag contents with colour coding"""
        contents = self.get_contents()
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}LETTER BAG STATUS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        if contents["available"]:
            print(f"{Fore.WHITE}Available in bag ({len(contents['available'])}): {' '.join(contents['available'])}{Style.RESET_ALL}")
        else:
            print(f"{Fore.WHITE}No letters available in bag{Style.RESET_ALL}")
        
        if contents["yellow"]:
            print(f"{Fore.YELLOW}Yellow letters (returned): {' '.join(contents['yellow'])}{Style.RESET_ALL}")
        
        if contents["green"]:
            print(f"{Fore.GREEN}Green letters (locked): {' '.join(contents['green'])}{Style.RESET_ALL}")
        
        if contents["removed"]:
            print(f"{Fore.RED}Red letters (removed): {' '.join(contents['removed'])}{Style.RESET_ALL}")
        
        if self.pulled_history:
            history = " → ".join(self.pulled_history[-10:])
            print(f"\nPull history (last 10): {history}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def can_pull(self) -> bool:
        """Check if any letters are available to pull"""
        return len(self._get_available_pullable_letters()) > 0