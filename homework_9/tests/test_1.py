"""
Unit tests for `merge_sorted_files`
from module `homework_9.tasks.task_1`.
"""
from pathlib import Path

import pytest

from homework_9.tasks.task_1 import merge_sorted_files

ONE_THREE_FIVE_LINES = "1\n3\n5\n"
TWO_FOUR_SIX_LINES = "2\n4\n6"
THREE_EMPTY_LINES = "\n\n\n"
EMPTY = ""


@pytest.fixture
def test_files_creator(tmp_path):
    """
    Creates file paths to the:

    + "one_three_five_lines.txt" with `ONE_THREE_FIVE_LINES`
    + "two_four_six_lines.txt" with `TWO_FOUR_SIX_LINES`
    + "three_empty_lines.py" with `THREE_EMPTY_LINES`
    + "empty.py" with `EMPTY`
    """
    test_dir = tmp_path / "tmp_dir"
    test_dir.mkdir()

    one_three_five_lines_txt = test_dir / "one_three_five_lines.txt"
    two_four_six_lines_txt = test_dir / "two_four_six_lines.txt"
    three_empty_lines_py = test_dir / "three_empty_lines.py"
    empty_py = test_dir / "empty.py"

    file_content = {
        one_three_five_lines_txt: ONE_THREE_FIVE_LINES,
        two_four_six_lines_txt: TWO_FOUR_SIX_LINES,
        three_empty_lines_py: THREE_EMPTY_LINES,
        empty_py: EMPTY,
    }

    for file, content in file_content.items():
        file.write_text(content)

    return (
        one_three_five_lines_txt,
        two_four_six_lines_txt,
        three_empty_lines_py,
        empty_py,
    )


# pylint: disable=redefined-outer-name


def test_single_file(test_files_creator):
    """
    Passes test if `merge_sorted_files` works correctly
    on the one sorted file with integers per lines.
    """
    one_three_five_lines_txt, _, _, _ = test_files_creator
    assert list(merge_sorted_files([one_three_five_lines_txt])) == [1, 3, 5]


def test_multiple_files(test_files_creator):
    """
    Passes test if `merge_sorted_files` works correctly
    on the sorted files with integers per lines.
    """
    one_three_five_lines_txt, two_four_six_lines_txt, _, _ = test_files_creator
    result = merge_sorted_files(
        [one_three_five_lines_txt, Path(two_four_six_lines_txt)]
    )
    assert list(result) == [1, 2, 3, 4, 5, 6]


def test_empty_lines_file(test_files_creator):
    """
    Passes test if `merge_sorted_files` yields
    nothing for the file with empty lines.
    """
    _, _, three_empty_lines_py, _ = test_files_creator
    assert list(merge_sorted_files([three_empty_lines_py])) == []


def test_empty_file(test_files_creator):
    """
    Passes test if `merge_sorted_files`
    yields nothing for the empty file.
    """
    _, _, _, empty_py = test_files_creator
    assert list(merge_sorted_files([empty_py])) == []
