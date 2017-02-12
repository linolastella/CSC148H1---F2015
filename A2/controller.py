# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete, hint_by_depth


class Tree:
    """Class responsible to store the puzzle state and actions that reach the
    state from the starting puzzle. Each node in the tree is organized as
    follows: (puzzle, parent, [actions], {children}), where puzzle is the Puzzle
    in this node, parent is the parent node of this node, [actions] is a list of
    actions taken from the current node, in ascending time order, {children} is
    a dictionary of children (action->node mapping) of this node.
    """

    # === Private Attributes ===
    # @type _curr: a tuple as described above.
    #    The current node in the state tree.
    #    It is initialized as (init, None, [], {}) as the root of the tree.
    def __init__(self, init):
        """Initialize a new Tree.

        @type self: Tree
        @type init: Puzzle
        @rtype: None
        """
        self._curr = (init, None, [], {})

    def act(self, action, state):
        """If the action is in the tree, simply move into that tree node.
        Otherwise, construct a new tree node tuple and add it as the
        child of the current node, then move into that node.

        @type self: Tree
        @type action: str
        @type state: Puzzle
        @rtype: None
        """
        if action in self._curr[3]:
            # Already made this action, move into directly.
            self._curr = self._curr[3][action]
        else:
            # Create a new tree node.
            node = (state, self._curr, [], {})
            # Add as the child of current node
            self._curr[2].append(action)
            self._curr[3][action] = node
            # Move into that node
            self._curr = node

    def undo(self):
        """Move into the parent and return the state in the parent node.
        If no parent node (already root of the tree), return None.

        @type self: Tree
        @rtype: Puzzle | None
        """
        if self._curr[1] is not None:
            self._curr = self._curr[1]
            return self._curr[0]
        else:
            return None

    def attempts(self):
        """Print out all actions and states in ascending time order.

        @type self: Tree
        @rtype: None
        """
        for action in self._curr[2]:
            print("action: " + action)
            print("result:")
            print(str(self._curr[3][action][0]))
        if len(self._curr[2]) == 0:
            print("You reached this state for the first time.")
        print("")


class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller
    # @type _view: View
    #     The view associated with this game controller
    # @type _tree: Tree
    #     The state tree.

    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type self: Controller
        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        # Construct the state tree
        self._tree = Tree(puzzle)

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        # : Add to this method to handle different actions.
        if action == 'exit':
            return '', True

        elif action == ":SOLVE":
            solution = solve(self._puzzle)
            if solution is None:
                return "There is no solution for this Puzzle!", True
            else:
                return str(solution), True

        elif action == ":SOLVE-ALL":
            solutions = solve_complete(self._puzzle)
            if len(solutions) == 0:
                return "There are no solutions for this Puzzle!", True
            else:
                values = [str(solution) for solution in solutions]
                return "\n".join(values), True

        elif action == ":UNDO":
            value = self._tree.undo()
            if value is None:
                print("There is no previous state.")
            else:
                self._puzzle = value
            return str(self._puzzle), self._puzzle.is_solved()

        elif action == ":ATTEMPTS":
            self._tree.attempts()
            return str(self._puzzle), self._puzzle.is_solved()

        elif len(action) > 5 and action[0:6] == ":HINT ":
            n = action[6:]
            try:
                n = int(n)
                print(hint_by_depth(self._puzzle, n))
                print()
                return str(self._puzzle), self._puzzle.is_solved()
            except:
                return "Invalid action, please try again.", False

        else:
            # Parse the action to the puzzle and make the move
            try:
                value = self._puzzle.move(action)
                self._puzzle = value
                # add the state into the tree
                self._tree.act(action, self._puzzle)
                #
                return str(value), value.is_solved()
            except:
                return "Invalid action, please try again.", False


if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle

    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])

    # c1 = Controller(s)

    from word_ladder_puzzle import WordLadderPuzzle
    w = WordLadderPuzzle("make", "cure")

    c2 = Controller(w)
