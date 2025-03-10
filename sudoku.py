# sudoku.py

from random import choice


class Sudoku:
    """Represents a Sudoku puzzle with randomly generated cells and streaks."""

    def __init__(self, size: int):
        self.size = size
        self.grid_data = []  # The generated Sudoku grid
        self.vertical_streaks = [[] for _ in range(size)]  # Streaks for vertical clues
        self.horizontal_streaks = []  # Streaks for horizontal clues
        self.total_correct = 0  # Total number of cells with value 1

    def generate_grid(self):
        """
        Generates the Sudoku grid and calculates the vertical and horizontal streaks.
        :return: The generated grid data as a 2D list.
        """
        self._initialize_data_structures()
        vertical_counts = [0] * self.size

        for row_idx in range(self.size):
            row_data, horizontal_streak = self._generate_row(row_idx, vertical_counts)
            self.horizontal_streaks.append(horizontal_streak)
            self.grid_data.append(row_data)

        self._finalize_vertical_streaks(vertical_counts)
        self._pad_streaks()
        return self.grid_data

    def _initialize_data_structures(self):
        """Resets the data structures to prepare for grid generation."""
        self.grid_data.clear()
        self.vertical_streaks = [[] for _ in range(self.size)]
        self.horizontal_streaks.clear()
        self.total_correct = 0

    def _generate_row(self, row_idx, vertical_counts):
        """
        Generates a single row of the grid and calculates the horizontal streaks.
        :param row_idx: The index of the current row.
        :param vertical_counts: A list tracking vertical streak counts for each column.
        :return: A tuple containing the row data and the horizontal streaks for the row.
        """
        row_data = []
        horizontal_streak = []
        current_streak = 0

        for col_idx in range(self.size):
            cell_value = choice([0, 1, 1])  # Randomly choose 0 or 1, with a higher probability for 1
            row_data.append(cell_value)
            current_streak, vertical_counts = self._process_cell(
                cell_value, col_idx, current_streak, vertical_counts, horizontal_streak
            )

        # Finalize the horizontal streak for the row if it ends with a streak
        if current_streak > 0:
            horizontal_streak.append(current_streak)

        return row_data, horizontal_streak

    def _process_cell(self, cell_value, col_idx, current_streak, vertical_counts, horizontal_streak):
        """
        Processes a single cell in the grid, updating streaks and counts.
        :param cell_value: The value of the cell (0 or 1).
        :param col_idx: The column index of the cell.
        :param current_streak: The current streak in the row.
        :param vertical_counts: The list of vertical streak counts.
        :param horizontal_streak: The list of horizontal streaks for the current row.
        :return: The updated current streak and vertical counts.
        """
        if cell_value == 1:
            self.total_correct += 1
            current_streak += 1
            vertical_counts[col_idx] += 1
        else:
            if current_streak > 0:
                horizontal_streak.append(current_streak)
            current_streak = 0
            if vertical_counts[col_idx] > 0:
                self.vertical_streaks[col_idx].append(vertical_counts[col_idx])
                vertical_counts[col_idx] = 0

        return current_streak, vertical_counts

    def _finalize_vertical_streaks(self, vertical_counts):
        """
        Finalizes the vertical streaks by appending any remaining streak counts.
        :param vertical_counts: The list of vertical streak counts.
        """
        for col_idx in range(self.size):
            if vertical_counts[col_idx] > 0:
                self.vertical_streaks[col_idx].append(vertical_counts[col_idx])

    def _pad_streaks(self):
        """Pads the streaks with empty strings to ensure uniform length."""
        max_streak_length = max(len(streak) for streak in self.vertical_streaks)
        self.vertical_streaks = [self._pad_streak(streak, max_streak_length) for streak in self.vertical_streaks]
        self.horizontal_streaks = [self._pad_streak(streak, max_streak_length) for streak in self.horizontal_streaks]

    @staticmethod
    def _pad_streak(streak, max_length):
        """
        Pads a streak with empty strings to ensure it has the specified length.
        :param streak: The streak to pad.
        :param max_length: The target length for the streak.
        :return: The padded streak.
        """
        return streak + [""] * (max_length - len(streak))
