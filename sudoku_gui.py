# sudoku_gui.py

import tkinter as tk
from sudoku import Sudoku
from tkinter import messagebox

LIGHT_RED = "#FF7F7F"
LIGHT_BLUE = "light blue"
BACKGROUND_COLOR = "#D3D3D3"
BUTTON_FONT = ("Consolas", 15)
LABEL_FONT = ("Consolas", 10)


def display_sudoku(size: int):
    """Displays the Sudoku puzzle in a Tkinter window."""
    sudoku = Sudoku(size)
    grid_data = sudoku.generate_grid()

    root = tk.Tk()
    root.title("Sudoku Grid")
    root.configure(bg=BACKGROUND_COLOR)

    frame = tk.Frame(root, bg=BACKGROUND_COLOR, padx=10, pady=10)
    frame.pack(padx=10, pady=(0, 10))

    buttons = []
    errors_var = tk.IntVar(value=0)
    correct_var = tk.IntVar(value=0)

    _display_vertical_streaks(frame, sudoku, size)
    _display_instructions(frame, size)
    score_label = _create_score_label(frame, size, errors_var)

    def update_score():
        """Updates the error score label."""
        score_label.config(text=f"❌:{errors_var.get()}")

    for r in range(size):
        row_buttons = []
        for c in range(size):
            button = tk.Button(
                frame,
                text=" ",
                width=4,
                height=2,
                font=BUTTON_FONT,
                bg="white",
                fg="black",
                relief=tk.FLAT,
                command=lambda r=r, c=c: _update_button(
                    r, c, buttons, grid_data, errors_var, correct_var, sudoku, update_score
                ),
            )
            button.grid(row=r + 5, column=c, padx=1, pady=1)
            button.bind("<Button-3>", lambda e, r=r, c=c: right_click_button(r, c, buttons))
            row_buttons.append(button)

        _display_horizontal_streak(frame, sudoku, r, size)
        buttons.append(row_buttons)

    def check_completion():
        """Check if all correct grid buttons have been pressed."""
        if correct_var.get() == sudoku.total_correct:
            response = messagebox.askyesno(
                "Game Complete",
                f"Congratulations! You've completed the puzzle!"
                f"\nErrors made: {errors_var.get()}"
                f"\nDo you want to play again?",
            )
            root.destroy()
            return response
        return None

    def _update_button(row, col, buttons, grid_data, errors_var, correct_var, sudoku, update_score):
        """Updates the grid buttons to the requested input."""
        current_bg = buttons[row][col].cget("bg")
        if current_bg == "white":
            if grid_data[row][col] == 1:
                buttons[row][col].config(bg="black", fg="white")
                correct_var.set(correct_var.get() + 1)
                if check_completion() is False:
                    exit()
            else:
                buttons[row][col].config(bg=LIGHT_RED, fg="black")
                errors_var.set(errors_var.get() + 1)
                update_score()

    def right_click_button(row, col, buttons):
        """Handles right-click events on buttons."""
        bt = buttons[row][col]
        if bt.cget("bg") == "white":
            bt.config(bg=LIGHT_BLUE, fg="white")
        elif bt.cget("bg") == LIGHT_BLUE:
            bt.config(bg="white", fg="black")

    root.mainloop()


def _display_vertical_streaks(frame, sudoku, size):
    """Displays the vertical streaks above the grid."""
    max_vertical_rows = max(len(column) for column in sudoku.vertical_streaks)
    for row in range(max_vertical_rows):
        for col in range(size):
            vertical_streak = sudoku.vertical_streaks[col]
            value = vertical_streak[row] if row < len(vertical_streak) else ""
            label = tk.Label(frame, text=value, width=2, height=1, font=BUTTON_FONT, bg=BACKGROUND_COLOR)
            label.grid(row=row + 1, column=col, sticky="n")


def _display_instructions(frame, size):
    """Displays instructions for the player."""
    tk.Label(frame, text="L click: fill", font=LABEL_FONT, bg=BACKGROUND_COLOR).grid(row=0, column=size, sticky="w")
    tk.Label(frame, text="R click: blank", font=LABEL_FONT, bg=BACKGROUND_COLOR).grid(row=1, column=size,
                                                                                      sticky="w")


def _create_score_label(frame, size, errors_var):
    """Creates the error score label."""
    score_label = tk.Label(frame, text=f"❌:{errors_var.get()}", width=8, height=1, font=BUTTON_FONT,
                           bg=BACKGROUND_COLOR)
    score_label.grid(row=3, column=size)
    return score_label


def _display_horizontal_streak(frame, sudoku, row, size):
    """Displays the horizontal streaks to the right of the grid."""
    horizontal_streak = " ".join(map(str, sudoku.horizontal_streaks[row]))
    label = tk.Label(
        frame,
        text=horizontal_streak,
        width=min(len(horizontal_streak) + 2, 15),
        height=2,
        font=BUTTON_FONT,
        bg=BACKGROUND_COLOR,
    )
    label.grid(row=row + 5, column=size, sticky="w", padx=5)