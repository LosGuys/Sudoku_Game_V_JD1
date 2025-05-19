import random
import copy
from typing import List, Tuple
import numpy as np

def generate_puzzle(difficulty: str) -> Tuple[List[List[int]], List[List[int]]]:
    """Wrapper function to match the interface expected by main.py"""
    generator = SudokuGenerator()
    puzzle, solution = generator.generate_puzzle(difficulty)
    
    # Convert to numpy arrays as expected by main.py
    puzzle_array = np.array(puzzle)
    solution_array = np.array(solution)
    
    return puzzle_array.tolist(), solution_array.tolist()

class SudokuGenerator:
    def __init__(self):
        self.puzzle_pool = []  # Keep a pool of valid puzzles
        self.pool_size = 10    # Keep top N puzzles in pool
        
    def generate_base(self) -> List[List[int]]:
        """Generate a complete valid Sudoku grid"""
        base = [[0]*9 for _ in range(9)]
        self._fill_diagonal_boxes(base)
        self._fill_remaining(base, 0, 3)
        return base
    
    def _fill_diagonal_boxes(self, grid: List[List[int]]) -> None:
        """Fill the diagonal 3x3 boxes - these can be filled independently"""
        for i in range(0, 9, 3):
            self._fill_box(grid, i, i)
    
    def _fill_box(self, grid: List[List[int]], row: int, col: int) -> None:
        """Fill a 3x3 box with random numbers"""
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                grid[row + i][col + j] = nums.pop()
    
    def _fill_remaining(self, grid: List[List[int]], i: int, j: int) -> bool:
        """Fill remaining cells using backtracking"""
        if j >= 9 and i < 8:
            i += 1
            j = 0
        if i >= 9 and j >= 9:
            return True
        if i < 3:
            if j < 3:
                j = 3
        elif i < 6:
            if j == (i//3)*3:
                j += 3
        else:
            if j == 6:
                i += 1
                j = 0
                if i >= 9:
                    return True
        
        for num in range(1, 10):
            if self._is_safe(grid, i, j, num):
                grid[i][j] = num
                if self._fill_remaining(grid, i, j + 1):
                    return True
                grid[i][j] = 0
        return False
    
    def _is_safe(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if number is valid in given position"""
        # Check row
        if num in grid[row]:
            return False
            
        # Check column
        if num in (grid[i][col] for i in range(9)):
            return False
            
        # Check box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if grid[i][j] == num:
                    return False
        return True

    def remove_numbers(self, grid: List[List[int]], difficulty: str) -> None:
        """Remove numbers while maintaining uniqueness"""
        cells = [(i, j) for i in range(9) for j in range(9)]
        
        # Define difficulty levels
        cells_to_remove = {
            "debug": 1,
            "easy": 40,
            "medium": 50,
            "hard": 60
        }.get(difficulty, 40)
        
        # Remove numbers one by one, ensuring unique solution
        removed = 0
        random.shuffle(cells)
        for i, j in cells:
            if removed >= cells_to_remove:
                break
                
            backup = grid[i][j]
            grid[i][j] = 0
            
            # If removing this number creates multiple solutions, put it back
            grid_copy = copy.deepcopy(grid)
            if not self._has_unique_solution(grid_copy):
                grid[i][j] = backup
            else:
                removed += 1

    def _has_unique_solution(self, grid: List[List[int]]) -> bool:
        """Check if the grid has exactly one solution"""
        solutions = []
        def solve(g):
            if len(solutions) > 1:  # Stop if we found multiple solutions
                return
            
            if all(all(cell != 0 for cell in row) for row in g):
                solutions.append(copy.deepcopy(g))
                return
                
            row, col = next((i, j) for i in range(9) for j in range(9) if g[i][j] == 0)
            for num in range(1, 10):
                if self._is_safe(g, row, col, num):
                    g[row][col] = num
                    solve(g)
                    g[row][col] = 0
            
        solve(grid)
        return len(solutions) == 1

    def generate_puzzle(self, difficulty: str) -> Tuple[List[List[int]], List[List[int]]]:
        """Generate a Sudoku puzzle with solution"""
        solution = self.generate_base()
        puzzle = copy.deepcopy(solution)
        self.remove_numbers(puzzle, difficulty)
        return puzzle, solution

# Example usage
if __name__ == "__main__":
    generator = SudokuGenerator()
    
    # Generate and display a puzzle of each difficulty
    for difficulty in ["debug", "easy", "medium", "hard"]:
        puzzle, solution = generator.generate_puzzle(difficulty)
        print(f"{difficulty.capitalize()} Puzzle:")
        for row in puzzle:
            print(" ".join(str(num) for num in row))
        print("\n")
