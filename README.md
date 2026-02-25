# Wordle FSM - Console Wordle Game

A console-based implementation of the popular word-guessing game Wordle, built using a Finite State Machine (FSM) architecture without boolean state flags.

## Overview

This Wordle clone challenges players to guess a secret 5-letter word within 6 attempts. After each guess, the game provides feedback about which letters are in the secret word and which are in the correct position. The game is implemented using a clean Finite State Machine design, demonstrating state-based programming principles.

## Features

- **Finite State Machine Architecture**: Clean state transitions without boolean flags
- **6 Attempts**: Standard Wordle rules
- **Letter Feedback**: 
  - Shows letters present in the word (any position)
  - Shows letters in the correct position
- **Built-in Word List**: 26 common 5-letter words
- **Confirmation Steps**: Review and confirm guesses before scoring
- **Game Statistics**: View all attempts and final outcome
- **Simple Console Interface**: Easy to use menu system

## How to Play

1. Run the program
2. Select "Play a round of Wordle" from the main menu
3. Enter 5-letter guesses (type 'quit' to exit the round)
4. Confirm your guess when prompted
5. Receive feedback about your guess
6. Continue guessing until you win or run out of attempts
7. View your results and return to the main menu

## Game States

The game progresses through these FSM states:

- **WORD_ENTRY**: Player enters a 5-letter guess
- **CONFIRM**: Player confirms or rejects the guess
- **SCORE**: Records the guess and increments attempt counter
- **IS_WINNER**: Checks if the guess matches the secret word
- **REVIEW**: Provides feedback about letters and positions
- **CONFIRM_AFTER_REVIEW**: Transitions back to WORD_ENTRY
- **DISPLAY**: Shows final results when game ends

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

1. Download the `wordle_fsm.py` file
2. Make it executable (optional):
   ```bash
   chmod +x wordle_fsm.py
   ```
3. Run the program:
   ```bash
   python3 wordle_fsm.py
   ```
   or
   ```bash
   ./wordle_fsm.py
   ```

## Customization

You can modify the word list by editing the `WORD_LIST` variable in the source code:

```python
WORD_LIST = [
    "apple", "brave", "cigar", ...  # Add or remove words here
]
```

To set a specific secret word instead of a random one:
```python
game = Wordle(secret_word="your_word")
```

## Example Gameplay

```
=== Wordle FSM ===
1) Play a round of Wordle
2) Leave
Select an option (1‑2): 1

Enter a 5‑letter guess (or type 'quit' to exit round): apple
You entered 'apple'. Proceed? (y/n): y

--- Review ---
Letters in the word (any position): a, e, l, p
Letters in the correct position: a
----------------

Enter a 5‑letter guess (or type 'quit' to exit round): eagle
...
```

## Design Philosophy

The program demonstrates state-machine design principles:
- Each game state is explicitly defined as an enum
- State transitions are clear and predictable
- No boolean flags to track game status
- Each state has a single responsibility
- Easy to extend with new states or features

## Author

Connor Lonergan

## License

This project is open source and available for educational purposes.

