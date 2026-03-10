"""Game constants and configuration"""

import random
import string

# Game settings
MAX_ATTEMPTS = 6
WORD_LENGTH = 5

# Keyboard layout
KEYBOARD_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

# Colour hierarchy for letter status
COLOUR_HIERARCHY = {
    "WHITE": 0,
    "RED": 1,
    "YELLOW": 2,
    "GREEN": 3
}

def generate_secret_word() -> str:
    """
    Generate a random 5-letter word with no duplicate letters
    by randomly selecting 5 unique letters from the alphabet
    """
    # Get all lowercase letters
    alphabet = list(string.ascii_lowercase)
    
    # Shuffle to ensure randomness
    random.shuffle(alphabet)
    
    # Take first 5 letters (guaranteed unique because we're taking from the shuffled list)
    word = ''.join(alphabet[:WORD_LENGTH])
    
    return word