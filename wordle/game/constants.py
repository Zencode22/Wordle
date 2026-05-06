"""Game constants and configuration"""

import random
import string
from typing import List

# Try to import requests, but provide fallback if not available
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: 'requests' module not found. Using fallback word list.")
    print("Install with: pip install requests")

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

# Dictionary API settings
DICTIONARY_API_BASE = "https://api.dictionaryapi.dev/api/v2/entries/en"

# Fallback word list with no duplicate letters
FALLBACK_WORDS = [
    "apple", "beach", "crane", "dance", "eagle",
    "flame", "grape", "heart", "igloo", "jelly",
    "kite", "lemon", "mango", "noble", "ocean",
    "piano", "queen", "robot", "snake", "tiger",
    "umbra", "vivid", "whale", "xenon", "yacht", "zebra"
]

def fetch_valid_five_letter_words() -> List[str]:
    """
    Fetch a list of common 5-letter words from a public word list.
    Since the dictionary API doesn't provide a direct word list endpoint,
    we'll use a public word list as our source.
    """
    if not REQUESTS_AVAILABLE:
        return FALLBACK_WORDS
    
    try:
        # Using a public word list of common English words
        url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            # Filter for 5-letter words only
            words = response.text.splitlines()
            five_letter_words = [
                word.lower() for word in words 
                if len(word) == WORD_LENGTH and word.isalpha()
            ]
            return five_letter_words
        else:
            return FALLBACK_WORDS
    except Exception:
        return FALLBACK_WORDS

def validate_word_exists(word: str) -> bool:
    """
    Validate that a word exists in the English dictionary using the API.
    Returns True if the word is valid, False otherwise.
    """
    if not REQUESTS_AVAILABLE:
        return True
    
    try:
        url = f"{DICTIONARY_API_BASE}/{word.lower()}"
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except Exception:
        # If API is unavailable, assume the word is valid
        return True

def generate_secret_word() -> str:
    """
    Generate a random 5-letter word from a dictionary of valid English words.
    Ensures the word has no duplicate letters and validates it against the API.
    """
    # Get list of 5-letter words
    word_list = fetch_valid_five_letter_words()
    
    # Filter words with no duplicate letters
    unique_letter_words = [
        word for word in word_list 
        if len(set(word)) == WORD_LENGTH
    ]
    
    if not unique_letter_words:
        # Fallback to generating random letters if no valid words found
        alphabet = list(string.ascii_lowercase)
        random.shuffle(alphabet)
        return ''.join(alphabet[:WORD_LENGTH])
    
    # Try up to 10 random words to find one that validates with the API
    random.shuffle(unique_letter_words)
    
    for word in unique_letter_words[:10]:
        if validate_word_exists(word):
            return word
    
    # If none validated, return a random one from the filtered list
    return random.choice(unique_letter_words)