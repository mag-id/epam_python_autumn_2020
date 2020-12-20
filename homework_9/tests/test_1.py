"""
Unit tests for `merge_sorted_files`
from module `homework_9.tasks.task_1`.
"""
from pathlib import Path

import pytest

from homework_9.tasks.task_1 import merge_sorted_files

FIRST_CONTENT = "1\n3\n5\n"
SECOND_CONTENT = "2\n4\n6"
THIRD_CONTENT = "\n\n\n"
FOURTH_CONTENT = ""


@pytest.fixture
def test_files(tmp_path):
    """
    Creates file paths to the:

    + "first_file.txt" with `FIRST_CONTENT`
    + "second_file.txt" with `SECOND_CONTENT`
    + "third_file.py" with `THIRD_CONTENT`
    + "fourth_file.txt" with `FOURTH_CONTENT`
    """
    test_dir = tmp_path / "tmp_dir"
    test_dir.mkdir()

    first_file = test_dir / "first_file.txt"
    second_file = test_dir / "second_file.txt"
    third_file = test_dir / "third_file.py"
    fourth_file = test_dir / "fourth_file.py"

    file_content = {
        first_file: FIRST_CONTENT,
        second_file: SECOND_CONTENT,
        third_file: THIRD_CONTENT,
        fourth_file: FOURTH_CONTENT,
    }

    for file, content in file_content.items():
        file.write_text(content)

    return first_file, second_file, third_file, fourth_file


# pylint: disable=redefined-outer-name


def test_single_file(test_files):
    """
    Passes test if `merge_sorted_files` works correctly
    on the one sorted file with integers per lines.
    """
    first_file, _, _, _ = test_files
    assert list(merge_sorted_files([first_file])) == [1, 3, 5]


def test_multiple_files(test_files):
    """
    Passes test if `merge_sorted_files` works correctly
    on the sorted files with integers per lines.
    """
    first_file, second_file, _, _ = test_files
    result = merge_sorted_files([first_file, Path(second_file)])
    assert list(result) == [1, 2, 3, 4, 5, 6]


def test_empty_lines_file(test_files):
    """
    Passes test if `merge_sorted_files` yields
    nothing for the file with empty lines.
    """
    _, _, third_file, _ = test_files
    assert list(merge_sorted_files([third_file])) == []


def test_empty_file(test_files):
    """
    Passes test if `merge_sorted_files`
    yields nothing for the empty file.
    """
    _, _, _, fourth_file = test_files
    assert list(merge_sorted_files([fourth_file])) == []
