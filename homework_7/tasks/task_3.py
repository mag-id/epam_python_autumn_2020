"""
Given a Tic-Tac-Toe 3x3 board (can be unfinished).
Write a function that checks if the are some winners.
If there is "x" winner, function should return "x wins!"
If there is "o" winner, function should return "o wins!"
If there is a draw, function should return "draw!"
If board is unfinished, function should return "unfinished!"

Example:
    [[-, -, o],
     [-, x, o],
     [x, o, x]]
    Return value should be "unfinished!"

    [[-, -, o],
     [-, o, o],
     [x, x, x]]

     Return value should be "x wins!"
"""
from itertools import chain
from typing import List

ThreeChar = List[str]

# [0, 1, 2,
#  3, 4, 5
#  6, 7, 8]
WIN_COMBINATIONS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),  # rows
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),  # columns
    (0, 4, 8),
    (2, 4, 6),  # diagonals
)

O_SIGN = -1
EMPTY_SIGN = 0
X_SIGN = +1

DRAW = 0
UNFINISHED = 9

X_WINS = X_SIGN * 3
O_WINS = O_SIGN * 3

ENCODED = {
    "o": O_SIGN,
    "-": EMPTY_SIGN,
    "x": X_SIGN,
}

DECODED = {
    UNFINISHED: "unfinished!",
    X_WINS: "x wins!",
    O_WINS: "o wins!",
    DRAW: "draw!",
}


def tic_tac_toe_checker(board: List[ThreeChar]) -> str:
    """
    Takes a Tic-Tac-Toe 3x3 board and returns status of the game.

    Statuses:
    ---------
    + If there is "x" winner, function should return `"x wins!"`
    + If there is "o" winner, function should return `"o wins!"`
    + If there is a draw, function should return `"draw!"`
    + If board is unfinished, function should return `"unfinished!"`
    """
    return _get_status(_get_signs(board))


def _get_signs(board: List[ThreeChar]) -> List[int]:
    """
    Returns `board` `ENCODED` to the signs list.

    Encoding:
    ---------
    + "o" = -1
    + "-" = 0
    + "x" = +1

    See
    """
    return [ENCODED[char] for char in chain(*board)]


def _get_status(signs: List[int]) -> str:
    """
    Returns calculated and `DECODED` status of the `signs`.

    Decoding:
    ---------
    + "o wins!" = -3
    + "draw!" = 0
    + "x wins!" = +3
    + "unfinished!" = +9
    """
    for combination in WIN_COMBINATIONS:
        signs_sum = sum(signs[i] for i in combination)
        if signs_sum == X_WINS:
            return DECODED[X_WINS]
        if signs_sum == O_WINS:
            return DECODED[O_WINS]
    return DECODED[UNFINISHED if EMPTY_SIGN in signs else DRAW]
