#!/usr/bin/env python3
"""
Wordle Game with Dynamic Letter Bag
Main entry point for the application
"""

from utils.colours import init_colours
from ui.menu import MainMenu


def main():
    """Main entry point for the Wordle game"""
    # Initialize colour support
    init_colours()
    
    # Start the main menu
    MainMenu.show()


if __name__ == "__main__":
    main()