# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""
from puzzle import Puzzle


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None
    """
    if verbose:
        print(puzzle)
    if puzzle.is_solved():
        return puzzle
    else:
        for subpuzzle in puzzle.extensions():
            possible_solution = solve(subpuzzle, verbose)
            if possible_solution is not None:
                return possible_solution


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]
    """
    if verbose:
        print(puzzle)
    solutions = []
    if puzzle.is_solved():
        solutions.append(puzzle)
    else:
        for subpuzzle in puzzle.extensions():
            solutions.extend(solve_complete(subpuzzle, verbose))
    return solutions


def hint_by_depth(puzzle, n):
    """Return a hint for the given puzzle state.

    Precondition: n >= 1.

    If <puzzle> is already solved, return the string 'Already at a solution!'
    If <puzzle> cannot lead to a solution or other valid state within <n> moves,
    return the string 'No possible extensions!'

    @type puzzle: Puzzle
    @type n: int
    @rtype: str
    """
    if puzzle.is_solved():
        return "Already at a solution!"
    value = helper_hint_by_depth(puzzle, n)
    if not value:
        return "No possible extensions!"
    return puzzle.from_puzzles_to_move(puzzle, value[0])


def helper_hint_by_depth(puzzle, k):
    """A recursive helper function for *hint_by_depth*.

    @type puzzle: Puzzle
    @type k: int
    @rtype: (Puzzle, bool) | None
    """
    if puzzle.is_solved():
        return puzzle, True
    if k == 0:
        return puzzle, False
    extensions = puzzle.extensions()
    if not extensions:
        return None
    for ext in extensions:
        value = helper_hint_by_depth(ext, k - 1)
        # Found one that can result in the solution in k steps
        if value and value[1]:
            return ext, True
    for ext in extensions:
        value = helper_hint_by_depth(ext, k - 1)
        # Found one that can result in the solution after k steps
        if value:
            return ext, False
    return None
