# Wordle Game with Dynamic Letter Bag

A feature-rich Wordle implementation with a dynamic letter bag system that adds strategic depth to the classic game. Play directly in your command terminal.

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

## Quick Start

### Windows
1. Download and extract the ZIP file
2. Double-click `run_game.bat`
3. The game will install dependencies and start automatically

### Mac/Linux
1. Download and extract the ZIP file
2. Open terminal in the game folder
3. Make the script executable: `chmod +x run_game.sh`
4. Run: `./run_game.sh`

### Manual Start
If the launcher scripts don't work, you can run the game manually:

1. Clone the repository:
```bash
git clone https://github.com/Zencode22/Wordle.git
cd Wordle