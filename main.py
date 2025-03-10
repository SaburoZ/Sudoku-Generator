# main.py

from tkinter import simpledialog, messagebox
from sudoku_gui import display_sudoku


def sudoku_game():
    """Main game loop."""
    while True:
        try:
            sudoku_size = simpledialog.askstring("Sudoku Size", "Choose the Sudoku size (5-10)")
            sudoku_size = int(sudoku_size)
            if 5 <= sudoku_size <= 10:
                display_sudoku(sudoku_size)
            else:
                messagebox.showerror("Wrong Size", "Sudoku size should be from 5 to 10.")
        except (TypeError, ValueError):
            break


if __name__ == "__main__":
    sudoku_game()
