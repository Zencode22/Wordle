# Wordle Game with Dynamic Letter Bag

A feature-rich Wordle implementation with a dynamic letter bag system that adds strategic depth to the classic game.

## Features
- Classic Wordle gameplay with 5-letter words
- Dynamic letter bag containing all 26 letters
- Letters change status based on guesses:
  - 🟩 **GREEN**: Locked in place (removed from bag permanently)
  - 🟨 **YELLOW**: Returned to bag (can be pulled again)
  - 🟥 **RED**: Permanently removed from game
- Pull letters from the bag for hints
- Colour-coded keyboard and bag display
- Finite State Machine game flow
- Cross-platform colour support (Windows, macOS, Linux)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Zencode22/Wordle.git
cd Wordle