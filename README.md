# Sudoku Game

A Python-based Sudoku game with a graphical interface using Tkinter. Features multiple difficulty levels, dynamic puzzle generation, and real-time feedback.

## Installation

1. Clone the repository
2. Create a virtual environment:
```powershell
python -m venv sudoku_env
.\sudoku_env\Scripts\Activate.ps1
```

3. Install required packages:
```powershell
pip install -r requirements.txt
```

## Features

- Four difficulty levels (Debug, Easy, Medium, Hard)
- Dynamic puzzle generation using advanced algorithms
- Real-time input validation
- Partial solution checking with visual feedback
- Tab navigation between cells
- Multi-threaded puzzle generation for responsiveness
- Status updates and progress tracking
- Clean and intuitive interface

## Requirements

- Python 3.x
- Tkinter (included in standard Python installation)
- NumPy

## How to Run

```bash
python main.py
```

## Game Controls

- Use numbers 1-9 to fill cells
- Tab key to navigate between cells
- "Partial Check" to validate current progress (with color feedback)
- "Check Solution" to verify completed puzzle
- "New Game" to generate a fresh puzzle
- Select difficulty from the dropdown menu

## Difficulty Levels

- Debug: Only one number removed (for testing)
- Easy: ~40 numbers to fill
- Medium: ~50 numbers to fill
- Hard: ~60 numbers to fill

## Advanced Features

- Multi-threaded puzzle generation for better UI responsiveness
- Unique solution guarantee for all puzzles
- Real-time feedback with cell highlighting:
  - Light gray: Original puzzle numbers
  - Light green: Correct user inputs
  - Pink: Incorrect user inputs
  - White: Empty cells

## Development

The game uses a sophisticated puzzle generation algorithm that ensures:
- Each puzzle has exactly one solution
- Appropriate difficulty based on selected level
- Efficient generation using backtracking and optimization
- Multi-threading for responsive UI

## Author

losguys (2025)
