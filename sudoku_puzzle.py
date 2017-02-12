# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Sudoku puzzle module.

Here are the rules of Sudoku:

- The puzzle consists of an n-by-n grid, where n = 4, 9, 16, or 25.
  Each square contains a uppercase letter between A and the n-th letter
  of the alphabet, or is empty.
  For example, on a 4-by-4 Sudoku board, the available letters are
  A, B, C, or D. On a 25-by-25 board, every letter A-Y is available.
- The goal is to fill in all empty squares with available letters so that
  the board has the following property:
    - no two squares in the same row have the same letter
    - no two squares in the same column have the same letter
    - no two squares in the same *subsquare* has the same letter
  A *subsquare* is found by dividing the board evenly into sqrt(n)-by-sqrt(n)
  pieces. For example, a 4-by-4 board would have 4 subsquares: top left,
  top right, bottom left, bottom right.

Note that most, but not all, of the code is given to you already.
"""
from puzzle import Puzzle
from math import sqrt

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class SudokuPuzzle(Puzzle):
    """Implementation of a Sudoku puzzle."""
    # === Private Attributes ===
    # @type _n: int
    #     The size of the board. Must be 4, 9, 16, or 25.
    # @type _grid: list[list[str]]
    #     A representation of the Sudoku grid. Consists of a list of lists,
    #     where each inner list represents a row of the grid.
    #
    #     Each item of the inner list is either an uppercase letter,
    #     or is the empty string '', representing an empty square.
    #     Each letter must be between 'A' and the n-th letter of the alphabet.
    def __init__(self, grid):
        """Create a new Sudoku puzzle with an initial grid 'grid'.

        Precondition: <grid> is a valid Sudoku grid.

        @type self: SudokuPuzzle
        @type grid: list[list[str]]
        @rtype: None
        """
        self._n = len(grid)
        self._grid = grid

    def __str__(self):
        """Return a human-readable string representation of <self>.

        Note that the numbers at the top and left cycle 0-9,
        to help the user when they want to enter a move.

        @type self: SudokuPuzzle
        @rtype: str

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> print(s)
          01|23
         ------
        0|AB|CD
        1|DC|BA
         ------
        2| D|
        3|  |
        <BLANKLINE>
        """
        m = int(sqrt(self._n))
        s = ''
        # Column label
        s += '  '
        for col in range(self._n):
            s += str(col % 10)
            # Vertical divider
            if (col + 1) % m == 0 and col + 1 != self._n:
                s += '|'
        # Horizontal divider
        s += '\n ' + ('-' * (self._n + m)) + '\n'
        for i in range(self._n):
            # Row label
            s += str(i % 10) + '|'
            for j in range(self._n):
                cell = self._grid[i][j]
                if cell == '':
                    s += ' '
                else:
                    s += str(cell)
                # Vertical divider
                if (j + 1) % m == 0 and j + 1 != self._n:
                    s += '|'
            s = s.rstrip()
            s += '\n'

            # Horizontal divider
            if (i + 1) % m == 0 and i + 1 != self._n:
                s += ' ' + ('-' * (self._n + m)) + '\n'

        return s

    def is_solved(self):
        """Return whether <self> is solved.

        A Sudoku puzzle is solved if its state matches the criteria
        listed at the end of the puzzle description.

        @type self: SudokuPuzzle
        @rtype: bool

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        True
        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'D', 'A', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        False
        """
        # Check for empty cells
        for row in self._grid:
            if '' in row:
                return False

        # Check rows
        for row in self._grid:
            if sorted(row) != list(CHARS[:self._n]):
                return False

        # Check cols
        for i in range(self._n):
            # Note the use of a list comprehension here.
            if sorted([row[i] for row in self._grid]) != list(CHARS[:self._n]):
                return False

        # Check all subsquares
        m = int(sqrt(self._n))
        for x in range(0, self._n, m):
            for y in range(0, self._n, m):
                items = [self._grid[x + i][y + j]
                         for i in range(m)
                         for j in range(m)]

                if sorted(items) != list(CHARS[:self._n]):
                    return False

        # All checks passed
        return True

    def extensions(self):
        """Return list of extensions of <self>.

        This method picks the first empty cell (looking top-down,
        left-to-right) and returns a list of the new puzzle states
        obtained by filling in the empty cell with one of the
        available letters that does not violate any of the constraints
        listed in the problem description. (E.g., if there is
        already an 'A' in the row with the empty cell, this method should
        not try to fill in the cell with an 'A'.)

        If there are no empty cells, returns an empty list.

        @type self: SudokuPuzzle
        @rtype: list[SudokuPuzzle]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> lst = list(s.extensions())
        >>> len(lst)
        1
        >>> print(lst[0])
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|D
        3|DC|
        <BLANKLINE>
        """
        # Search for the first empty cell
        row_index, col_index = None, None
        for i in range(self._n):
            row = self._grid[i]
            if '' in row:
                row_index, col_index = i, row.index('')
                break

        if row_index is None:
            return []
        else:
            # Calculate possible letter to fill the empty cell
            letters = self._possible_letters(row_index, col_index)
            return [self._extend(letter, row_index, col_index)
                    for letter in letters]

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.
        Do *NOT* change the state of <self>. This is not a mutating method!

        @type self: SudokuPuzzle
        @type move: str
        @rtype: Puzzle
        """
        if self._is_valid(move):
            return self._extend(move[-1], int(move[1]), int(move[4]))
        else:
            raise ValueError

    def from_puzzles_to_move(self, puzzle1, puzzle2):
        """An helper function for *hint_by_depth* in the solver.py module.

        puzzle1 is the current puzzle state and puzzle2 is a puzzle state after
        a valid move. Return the move that leads from puzzle1 to puzzle2.

        @type self: SudokuPuzzle
        @type puzzle1: SudokuPuzzle
        @type puzzle2: SudokuPuzzle
        @rtype: str
        """
        for i in range(len(puzzle1._grid)):
            for j in range(len(puzzle1._grid)):
                if puzzle1._grid[i][j] != puzzle2._grid[i][j]:
                    move = (i, j, (puzzle2._grid[i][j]))
        return '({}, {}) -> {}'.format(move[0], move[1], move[-1])

    # ------------------------------------------------------------------------
    # Helpers for methods 'extensions' and 'move'
    # ------------------------------------------------------------------------
    def _possible_letters(self, row_index, col_index):
        """Return a list of possible letters for a cell.

        The returned letters must be a subset of the available letters.
        The returned list should be sorted in alphabetical order.

        @type self: SudokuPuzzle
        @type row_index: int
        @type col_index: int
        @rtype: list[str]
        """
        letters = list(CHARS[:self._n])

        # Remove all the letters from the same row
        for letter in self._grid[row_index]:
            if letter in letters:
                letters.remove(letter)

        # Remove all the letters from the same column
        for i in range(self._n):
            if self._grid[i][col_index] in letters:
                letters.remove(self._grid[i][col_index])

        # Remove all the letters from the subsquare
        m = int(sqrt(self._n))
        x = row_index // m * m
        y = col_index // m * m
        items = [self._grid[x + i][y + j] for i in range(m) for j in range(m)]
        for item in items:
            if item in letters:
                letters.remove(item)

        return letters

    def _extend(self, letter, row_index, col_index):
        """Return a new Sudoku puzzle obtained after one move.

        The new puzzle is identical to <self>, except that it has
        the value at position (row_index, col_index) equal to 'letter'
        instead of empty.

        'letter' must be an available letter.
        'row_index' and 'col_index' are between 0-3.

        @type self: SudokuPuzzle
        @type letter: str
        @type row_index: int
        @type col_index: int
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> print(s._extend('B', 2, 3))
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA| B
        3|DC|
        <BLANKLINE>
        """
        new_grid = [row.copy() for row in self._grid]
        new_grid[row_index][col_index] = letter
        return SudokuPuzzle(new_grid)

    def _is_valid(self, move):
        """Return True if and only if <move> is a valid move for the sudoku
        puzzle <self>.

        @type self: SudokuPuzzle
        @type move: str
        @rtype: Bool
        """
        # Check if format is correct.
        if len(move) != 11 or not move.startswith('(') or \
                move[2:4] != ', ' or move[5:10] != ') -> ' or not \
                move[-1].isupper()or not move[1].isdigit() or not \
                move[4].isdigit():
            return False

        # Check if the cell is a valid cell.
        if self._grid[int(move[1])][int(move[4])] != '':
            return False

        # Check if the input is a valid input.
        if int(move[1]) < 0 or int(move[1]) >= self._n or int(move[4]) < 0 or \
            int(move[4]) >= self._n or not \
                move[-1] in self._possible_letters(int(move[1]), int(move[4])):
                return False

        # All the tests passed, then <move> is a valid move.
        return True
