# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Word ladder module.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it?

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""

    # === Private attributes ===
    # @type _words: list[str]
    #     List of allowed English words
    # @type _start: str
    #     The start word
    # @type _target: str
    #     The target word
    # @type _states: list[str]
    #     List of words that have been tried.

    def __init__(self, start, target, states=None, words=None):
        """Create a new word ladder puzzle with given start and target words.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @type states: list[str] | None
        @type words: list[str] | None
        @rtype: None
        """
        # Code to initialize _words - you don't need to change this.
        if words is None:
            self._words = []
            with open('wordsEnTest.txt') as wordfile:
                for line in wordfile:
                    self._words.append(line.strip())
            self._words = set(self._words)
        else:
            self._words = words

        self._start = start
        self._target = target
        self._states = []
        if states is not None:
            self._states.extend(states)

    def __str__(self):
        """Return a human-readable string representation of <self>.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> w = WordLadderPuzzle('make', 'cure')
        >>> w._ladder = ['make', 'cake', 'care', 'cure']
        >>> print(w)
        make -> cake -> care -> cure
        """
        string = " -> ".join(self._states + [self._start])
        if not self.is_solved():
            string += " -> ??? -> " + self._target
        return string

    def is_solved(self):
        """Return whether this puzzle is in a solved state.

        A word ladder puzzle is solved when the target word is reached.

        @type self: WordLadderPuzzle
        @rtype: bool
        """
        return self._start == self._target

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        """
        lst = []

        # Change each character in the start word and if the resulting word is
        # in the dictionary (not in the history), add it to the list.
        chars = list(self._start)
        for i in range(len(chars)):
            origin = chars[i]
            for k in CHARS:
                if k != origin:
                    chars[i] = k
                    word = "".join(chars)
                    if word not in lst and word not in self._states \
                            and word in self._words:
                        lst.append(word)
            chars[i] = origin

        # Now construct the extensions with the word in the list.
        extentions = []
        states = self._states + [self._start]
        for word in sorted(lst):
            extentions.append(WordLadderPuzzle(word, self._target, states,
                                               self._words))
        return extentions

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: WordLadderPuzzle
        """
        # Check if the word in the move is valid
        possibles = [state._start for state in self.extensions()]
        if move in possibles:
            return WordLadderPuzzle(move, self._target, self._states +
                                    [self._start])
        else:
            raise ValueError

    def from_puzzles_to_move(self, puzzle1, puzzle2):
        """An helper function for *hint_by_depth* in the solver.py module.

        puzzle1 is the current puzzle state and puzzle2 is a puzzle state after
        a valid move. Return the move that leads from puzzle1 to puzzle2.

        @type self: WordLadderPuzzle
        @type puzzle1: WordLadderPuzzle
        @type puzzle2: WordLadderPuzzle
        @rtype: str
        """
        words = str(puzzle2).split(' -> ')
        return words[words.index('???') - 1]
