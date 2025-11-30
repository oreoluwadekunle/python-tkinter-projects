# Guess the number

A Python Tkinter-based number guessing game with single-player and multiplayer modes.

## Features

### Single Player Mode

- Guess a randomly selected number within a configurable range
- Multiple difficulty presets (Easy, Medium, Hard, Custom)
- Real-time timer tracking elapsed time
- Hints system with progressive information
- Score calculation based on attempts, hints used, and time taken
- Leaderboard system with separate rankings for each difficulty

### Multiplayer Mode

- Add multiple players (minimum 2 required)
- Turn-based gameplay where each player gets a chance to guess
- Players are automatically cycled through until one finds the number
- Real-time score tracking for all players
- Scoring system: bonus points for finding the number quickly
- Final results displayed with medal rankings (🥇 🥈 🥉)
- Configurable game settings (number range, max attempts)

### Leaderboard

- Separate leaderboards for each difficulty level
- Top 10 scores displayed with player names
- Medal system for top 3 players
- Clear difficulty-specific leaderboards

## How to Play

### Single Player

1. Open the Settings tab
2. Choose a difficulty (Easy, Medium, Hard) or set Custom settings
3. Click "Start Game"
4. Guess numbers and use the number pad to input guesses
5. Use hints strategically (Hint button)
6. When you guess correctly, enter your name to save your score

### Multiplayer

1. Click on the "Multiplayer" tab
2. Add player names one by one using the Player Name field
3. (Optional) Adjust game settings (default: 1-100, 10 attempts)
4. Click "Start Multiplayer Game"
5. Players take turns guessing in order
6. First player to guess the number wins!
7. Game displays final scores with rankings

## Requirements

- Python 3.7+
- tkinter (usually comes with Python)
- pygame (for background music)

## Installation

```bash
pip install pygame
```

## Files

- `gtn.py` - Original single-player version
- `gtn_multiplayer.py` - Single-player + Multiplayer version (recommended)
- `leaderboard.json` - Stores high scores data

## Running the Game

```bash
python gtn_multiplayer.py
```

Or double-click `run_game.bat` (Windows) or `run_game.command` (macOS)

## Created by

Adekunle Oreoluwa
