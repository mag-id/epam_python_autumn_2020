"""
Unit tests for `universal_file_counter`
from module `homework_9.tasks.task_3`.
"""

from pathlib import Path
from typing import Callable

import pytest

from homework_9.tasks.task_3 import universal_file_counter

FIRST_CONTENT = "1\n2\n3\n"
SECOND_CONTENT = "4 5\n6 7\n 9 10"
THIRD_CONTENT = "\n\n\n"
FOURTH_CONTENT = ""


@pytest.fixture
def test_files(tmp_path):
    """
    Creates temporary direcory with 4 text files:

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
def test_no_tokenizer(test_files, file_extension: str, expected_result: int):
    """
    Passes test if result without `tokenizer` is equal to `expected_result`.
    """
    assert universal_file_counter(Path(test_files), file_extension) == expected_result


@pytest.mark.parametrize(
    ["file_extension", "tokenizer", "expected_result"],
    [
        pytest.param("txt", lambda line: line.split(), 9),
        pytest.param("py", lambda line: line.split(), 0),
        pytest.param(".txt", lambda line: line.split(), 9),
        pytest.param(".py", lambda line: line.split(), 0),
    ],
)
def test_with_tokenizer(
    test_files, file_extension: str, tokenizer: Callable, expected_result: int
):
    """
    Passes test if result with `tokenizer` is equal to `expected_result`.
    """
    assert (
        universal_file_counter(Path(test_files), file_extension, tokenizer)
        == expected_result
    )
