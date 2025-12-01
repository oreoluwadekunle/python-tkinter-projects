# 🎮 Guess The Number

[Download Latest Version](https://github.com/oreoluwadekunle/python-tkinter-projects/releases/latest)

A Python Tkinter-based number guessing game with single-player mode

## Features

### Single Player Mode

- Guess a randomly selected number within a configurable range
- Multiple difficulty presets (Easy, Medium, Hard, Custom)
- Real-time timer tracking elapsed time
- Hints system with progressive information
- Score calculation based on attempts, hints used, and time taken
- Leaderboard system with separate rankings for each difficulty

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
- `leaderboard.json` - Stores high scores data
- `game_history.json` - Stores all scores data
- `streak.json` - Stores player's winning streaks

## Running the Game

```bash
python gtn.py
```

Or double-click `run_game.bat` (Windows) or `run_game.command` (macOS)

## Created by

Adekunle Oreoluwa
