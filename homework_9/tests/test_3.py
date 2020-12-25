"""
Unit tests for `universal_file_counter`
from module `homework_9.tasks.task_3`.
"""

from pathlib import Path

import pytest

from homework_9.tasks.task_3 import universal_file_counter

ONE_LINE_ONE_INTEGER = "1\n2\n3\n"
ONE_LINE_TWO_INTEGERS = "4 5\n6 7\n 9 10"
THREE_EMPTY_LINES = "\n\n\n"
EMPTY = ""


@pytest.fixture
def test_files_creator(tmp_path):
    """
    Creates temporary direcory with 4 text files:

    + "one_line_one_integer.txt" with `ONE_LINE_ONE_INTEGER`
    + "one_line_two_integers.txt" with `ONE_LINE_TWO_INTEGERS`
    + "three_empty_lines.py" with `THREE_EMPTY_LINES`
    + "empty.py" with `EMPTY`
    """
    test_dir = tmp_path / "tmp_dir"
    test_dir.mkdir()

    one_line_one_integer_txt = test_dir / "one_line_one_integer.txt"
    one_line_two_integers_txt = test_dir / "one_line_two_integers.txt"
    three_empty_lines_py = test_dir / "three_empty_lines.py"
    empty_py = test_dir / "empty.py"

    file_content = {
        one_line_one_integer_txt: ONE_LINE_ONE_INTEGER,
        one_line_two_integers_txt: ONE_LINE_TWO_INTEGERS,
        three_empty_lines_py: THREE_EMPTY_LINES,
        empty_py: EMPTY,
    }

    for file, content in file_content.items():
        file.write_text(content)

    return test_dir


# pylint: disable=redefined-outer-name


@pytest.mark.parametrize(
    ["file_extension", "expected_result"],
    [
        pytest.param("txt", 6),
        pytest.param("py", 3),
        pytest.param(".txt", 6),
        pytest.param(".py", 3),
    ],
)
def test_no_tokenizer(test_files_creator, file_extension: str, expected_result: int):
    """
    Passes test if result without `tokenizer` is equal to `expected_result`.
    """
    assert (
        universal_file_counter(Path(test_files_creator), file_extension)
        == expected_result
    )


@pytest.mark.parametrize(
    ["file_extension", "expected_result"],
    [
        pytest.param("txt", 9),
        pytest.param("py", 0),
        pytest.param(".txt", 9),
        pytest.param(".py", 0),
    ],
)
def test_with_tokenizer(test_files_creator, file_extension: str, expected_result: int):
    """
    Passes test if result with `str.split` `tokenizer` is equal to `expected_result`.
    """
    assert (
        universal_file_counter(Path(test_files_creator), file_extension, str.split)
        == expected_result
    )
