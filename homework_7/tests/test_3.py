"""
Unit tests for module `homework_7.tasks.task_3`.
"""
from typing import List

import pytest

from homework_7.tasks.task_3 import _get_signs, _get_status, tic_tac_toe_checker

ThreeChar = List[str]


@pytest.mark.parametrize(
    ["board", "expected_status"],
    [
        pytest.param(
            [
                ["-", "-", "o"],
                ["-", "x", "o"],
                ["x", "o", "x"],
            ],
            "unfinished!",
        ),
        pytest.param(
            [
                ["-", "-", "o"],
                ["-", "o", "o"],
                ["x", "x", "x"],
            ],
            "x wins!",
        ),
        pytest.param(
            [
                ["o", "-", "o"],
                ["-", "o", "x"],
                ["x", "o", "o"],
            ],
            "o wins!",
        ),
        pytest.param(
            [
                ["x", "x", "o"],
                ["o", "o", "x"],
                ["x", "o", "o"],
            ],
            "draw!",
        ),
    ],
)
def test_tic_tac_toe_checker(board: List[ThreeChar], expected_status: str):
    """
    Passes test if `tic_tac_toe_checker(board)` is equal to `expected_status`.
    """
    assert tic_tac_toe_checker(board) == expected_status


@pytest.mark.parametrize(
    ["board", "expected_signs"],
    [
        pytest.param(
            [
                ["-", "-", "o"],
                ["-", "x", "o"],
                ["x", "o", "x"],
            ],
            [0, 0, -1, 0, 1, -1, 1, -1, 1],
        ),
        pytest.param(
            [
                ["-", "-", "o"],
                ["-", "o", "o"],
                ["x", "x", "x"],
            ],
            [0, 0, -1, 0, -1, -1, 1, 1, 1],
        ),
    ],
)
def test_get_signs(board: List[ThreeChar], expected_signs: List[int]):
    """
    Passes test if `_get_signs(board)` is equal to `expected_signs`.
    """
    assert _get_signs(board) == expected_signs


@pytest.mark.parametrize(
    ["signs", "expected_status"],
    [
        pytest.param(
            [0, 0, -1, 0, 1, -1, 1, -1, 1],
            "unfinished!",
        ),
        pytest.param(
            [0, 0, -1, 0, -1, -1, 1, 1, 1],
            "x wins!",
        ),
    ],
)
def test_get_status(signs: List[int], expected_status: str):
    """
    Passes test if `_get_status(signs)` is equal to `expected_status`.
    """
    assert _get_status(signs) == expected_status
