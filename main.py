import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sudoku_generator import generate_puzzle
import threading

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.cells = {}
        self.current_puzzle = None
        self.solution = None
        self.loading = False
        
        # Create menu and difficulty selector
        self.create_menu()
        
        # Create game board
        self.create_board()
        
        # Create status label
        self.status_label = tk.Label(self.root, text="", font=('Arial', 12), pady=10)
        self.status_label.pack(side=tk.BOTTOM)
        
        # Load first puzzle
        self.load_new_puzzle()

    def create_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=5)
        
        # Difficulty selector
        difficulty_frame = tk.Frame(menu_frame)
        difficulty_frame.pack(side=tk.TOP, pady=5)
        
        tk.Label(difficulty_frame, text="Difficulty:").pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="medium")
        difficulty_combo = ttk.Combobox(
            difficulty_frame, 
            textvariable=self.difficulty_var,
            values=["debug", "easy", "medium", "hard"],
            state="readonly",
            width=10
        )
        difficulty_combo.pack(side=tk.LEFT, padx=5)
        
        # Buttons and loading indicator
        button_frame = tk.Frame(menu_frame)
        button_frame.pack(side=tk.TOP, pady=5)
        
        self.new_game_btn = tk.Button(button_frame, text="New Game", command=self.load_new_puzzle)
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        partial_check_btn = tk.Button(button_frame, text="Partial Check", command=self.partial_check)
        partial_check_btn.pack(side=tk.LEFT, padx=5)
        
        check_btn = tk.Button(button_frame, text="Check Solution", command=self.check_solution)
        check_btn.pack(side=tk.LEFT, padx=5)
        
        self.loading_label = tk.Label(button_frame, text="Generating puzzle...", fg="blue")
        # Loading label is initially hidden
        self.loading_label.pack(side=tk.LEFT, padx=5)
        self.loading_label.pack_forget()

    def create_board(self):
        # Clear only the board frame before creating a new board
        if hasattr(self, 'board_frame'):
            self.board_frame.destroy()

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=20, pady=20)  # Increased padding

        for i in range(9):
            for j in range(9):
                cell_frame = tk.Frame(
                    self.board_frame,
                    borderwidth=1,
                    relief="solid",
                    width=50,  # Fixed width
                    height=50,  # Fixed height
                )
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                cell_frame.grid_propagate(False)  # Maintain fixed size

                cell = tk.Entry(
                    cell_frame,
                    width=2,
                    font=('Arial', 24),  # Larger font
                    justify='center',
                    bg='white'  # White background
                )
                cell.place(relx=0.5, rely=0.5, anchor='center')  # Center in frame

                # Add thicker borders for 3x3 boxes
                if i % 3 == 0 and i != 0:
                    cell_frame.grid(pady=(3, 1))
                if j % 3 == 0 and j != 0:
                    cell_frame.grid(padx=(3, 1))

                # Bind both keypress and keyrelease for better input control
                cell.bind('<KeyPress>', lambda e, i=i, j=j: self.validate_input(e, i, j))
                cell.bind('<KeyRelease>', lambda e, i=i, j=j: self.post_validate_input(e, i, j))
                self.cells[(i, j)] = cell

    def validate_input(self, event, i, j):
        """Pre-validate input before it's entered"""
        if event.char:
            # Only allow digits 1-9
            if not event.char.isdigit() or event.char == '0':
                return "break"
            # Clear existing content and allow new input
            if self.cells[(i, j)].get():
                self.cells[(i, j)].delete(0, tk.END)
        return None

    def post_validate_input(self, event, i, j):
        """Clean up input after it's entered"""
        cell = self.cells[(i, j)]
        value = cell.get()
        
        # Handle backspace/delete
        if not value:
            return
            
        # Ensure single digit 1-9
        if not value.isdigit() or int(value) < 1 or int(value) > 9:
            cell.delete(0, tk.END)
            return
            
        # Ensure only one digit
        if len(value) > 1:
            cell.delete(1, tk.END)

    def load_new_puzzle(self):
        if self.loading:
            return
        
        self.loading = True
        self.new_game_btn.config(state='disabled')
        self.loading_label.pack(side=tk.LEFT, padx=5)
        self.status_label.config(text="")  # Clear status when starting new game
        
        def generate():
            # Generate new puzzle with selected difficulty
            difficulty = self.difficulty_var.get()
            puzzle, solution = generate_puzzle(difficulty)
            
            # Save to files in background
            with open(f"{difficulty}_puzzle.txt", "w") as puzzle_file:
                for row in puzzle:
                    puzzle_file.write(" ".join(map(str, row)) + "\n")

            with open(f"{difficulty}_solution.txt", "w") as solution_file:
                for row in solution:
                    solution_file.write(" ".join(map(str, row)) + "\n")
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_board(puzzle, solution))
        
        # Start generation in separate thread
        thread = threading.Thread(target=generate)
        thread.daemon = True  # Thread will close when main program exits
        thread.start()
    
    def update_board(self, puzzle, solution):
        """Update the board with a new puzzle (called in main thread)"""
        self.current_puzzle = puzzle
        self.solution = solution
        
        # Recreate the board with new puzzle
        self.create_board()
        
        # Fill the board
        for i in range(9):
            for j in range(9):
                value = puzzle[i][j]
                cell = self.cells[(i, j)]
                if value != 0:
                    cell.insert(0, str(value))
                    cell.config(bg='lightgray')
        
        # Re-enable new game button and hide loading label
        self.loading = False
        self.new_game_btn.config(state='normal')
        self.loading_label.pack_forget()
        
        # Setup tab navigation
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                next_i, next_j = (i, j + 1) if j < 8 else (i + 1, 0)
                if next_i < 9:
                    cell.bind('<Tab>', lambda e, ni=next_i, nj=next_j: self.focus_next_cell(ni, nj))

    def create_board(self):
        # Clear only the board frame before creating a new board
        if hasattr(self, 'board_frame'):
            self.board_frame.destroy()

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=20, pady=20)  # Increased padding

        for i in range(9):
            for j in range(9):
                cell_frame = tk.Frame(
                    self.board_frame,
                    borderwidth=1,
                    relief="solid",
                    width=50,  # Fixed width
                    height=50,  # Fixed height
                )
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                cell_frame.grid_propagate(False)  # Maintain fixed size

                cell = tk.Entry(
                    cell_frame,
                    width=2,
                    font=('Arial', 24),  # Larger font
                    justify='center',
                    bg='white'  # White background
                )
                cell.place(relx=0.5, rely=0.5, anchor='center')  # Center in frame

                # Add thicker borders for 3x3 boxes
                if i % 3 == 0 and i != 0:
                    cell_frame.grid(pady=(3, 1))
                if j % 3 == 0 and j != 0:
                    cell_frame.grid(padx=(3, 1))

                # Bind both keypress and keyrelease for better input control
                cell.bind('<KeyPress>', lambda e, i=i, j=j: self.validate_input(e, i, j))
                cell.bind('<KeyRelease>', lambda e, i=i, j=j: self.post_validate_input(e, i, j))
                self.cells[(i, j)] = cell

    def validate_input(self, event, i, j):
        """Pre-validate input before it's entered"""
        if event.char:
            # Only allow digits 1-9
            if not event.char.isdigit() or event.char == '0':
                return "break"
            # Clear existing content and allow new input
            if self.cells[(i, j)].get():
                self.cells[(i, j)].delete(0, tk.END)
        return None

    def post_validate_input(self, event, i, j):
        """Clean up input after it's entered"""
        cell = self.cells[(i, j)]
        value = cell.get()
        
        # Handle backspace/delete
        if not value:
            return
            
        # Ensure single digit 1-9
        if not value.isdigit() or int(value) < 1 or int(value) > 9:
            cell.delete(0, tk.END)
            return
            
        # Ensure only one digit
        if len(value) > 1:
            cell.delete(1, tk.END)

    def load_new_puzzle(self):
        if self.loading:
            return
        
        self.loading = True
        self.new_game_btn.config(state='disabled')
        self.loading_label.pack(side=tk.LEFT, padx=5)
        self.status_label.config(text="")  # Clear status when starting new game
        
        def generate():
            # Generate new puzzle with selected difficulty
            difficulty = self.difficulty_var.get()
            puzzle, solution = generate_puzzle(difficulty)
            
            # Save to files in background
            with open(f"{difficulty}_puzzle.txt", "w") as puzzle_file:
                for row in puzzle:
                    puzzle_file.write(" ".join(map(str, row)) + "\n")

            with open(f"{difficulty}_solution.txt", "w") as solution_file:
                for row in solution:
                    solution_file.write(" ".join(map(str, row)) + "\n")
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_board(puzzle, solution))
        
        # Start generation in separate thread
        thread = threading.Thread(target=generate)
        thread.daemon = True  # Thread will close when main program exits
        thread.start()
    
    def update_board(self, puzzle, solution):
        """Update the board with a new puzzle (called in main thread)"""
        self.current_puzzle = puzzle
        self.solution = solution
        
        # Recreate the board with new puzzle
        self.create_board()
        
        # Fill the board
        for i in range(9):
            for j in range(9):
                value = puzzle[i][j]
                cell = self.cells[(i, j)]
                if value != 0:
                    cell.insert(0, str(value))
                    cell.config(bg='lightgray')
        
        # Re-enable new game button and hide loading label
        self.loading = False
        self.new_game_btn.config(state='normal')
        self.loading_label.pack_forget()
        
        # Setup tab navigation
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                next_i, next_j = (i, j + 1) if j < 8 else (i + 1, 0)
                if next_i < 9:
                    cell.bind('<Tab>', lambda e, ni=next_i, nj=next_j: self.focus_next_cell(ni, nj))

    def get_current_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[(i, j)].get()
                row.append(int(value) if value else 0)
            board.append(row)
        return board

    def check_solution(self):
        board = self.get_current_board()
        has_errors = False
        
        # Reset all cell colors first
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                cell.config(bg='white' if self.current_puzzle[i][j] == 0 else 'lightgray')
        
        # Check if board is complete
        if any(0 in row for row in board):
            self.status_label.config(text="Please fill in all cells!", fg='blue')
            return
            
        # Check each cell and highlight incorrect ones
        for i in range(9):
            for j in range(9):
                if board[i][j] != self.solution[i][j]:
                    self.cells[(i, j)].config(bg='pink')  # Highlight incorrect cells
                    has_errors = True
        
        # Update status label
        if not has_errors:
            self.status_label.config(text="Congratulations! You solved the puzzle correctly!", fg='green')
        else:
            self.status_label.config(text="The highlighted cells are incorrect. Keep trying!", fg='red')

    def partial_check(self):
        """Check only the cells that the user has filled in"""
        board = self.get_current_board()
        
        # Reset all cell colors first
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                cell.config(bg='white' if self.current_puzzle[i][j] == 0 else 'lightgray')
        
        wrong_count = 0
        correct_count = 0
        
        # Check only filled cells that were not pre-filled
        for i in range(9):
            for j in range(9):
                if self.current_puzzle[i][j] == 0 and board[i][j] != 0:
                    if board[i][j] == self.solution[i][j]:
                        self.cells[(i, j)].config(bg='lightgreen')  # Correct numbers in green
                        correct_count += 1
                    else:
                        self.cells[(i, j)].config(bg='pink')  # Wrong numbers in pink
                        wrong_count += 1
        
        # Update status label
        if correct_count + wrong_count == 0:
            self.status_label.config(text="No cells filled in yet!", fg='blue')
        else:
            self.status_label.config(
                text=f"Correct numbers: {correct_count} | Incorrect numbers: {wrong_count}",
                fg='black' if wrong_count == 0 else 'red'
            )

def main():
    root = tk.Tk()
    game = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
