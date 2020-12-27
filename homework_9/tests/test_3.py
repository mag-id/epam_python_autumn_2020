"""
Unit tests for `universal_file_counter`
from module `homework_9.tasks.task_3`.
"""

from pathlib import Path

import pytest

from homework_9.tasks.task_3 import universal_file_counter

# pylint: disable=unused-import
from homework_9.tests.fixtures import create_tmp_file, tmp_dir

# pylint: disable=redefined-outer-name


@pytest.fixture
def filled_tmp_dir(create_tmp_file, tmp_dir) -> Path:
    """
    Creates files with current `name`s, `content`s
    at `tmp_dir` and returns `Path` to the `tmp_dir`.
    """
    create_tmp_file("1_line_1_integer.txt", "1\n2\n3\n")
    create_tmp_file("1_line_2_integers.txt", "4 5\n6 7\n 9 10")
    create_tmp_file("3_empty_lines.py", "\n\n\n")
    create_tmp_file("empty.py", "")

    return tmp_dir


@pytest.mark.parametrize(
    ["file_extension", "expected_result"],
    [
        pytest.param("txt", 6),
        pytest.param("py", 3),
        pytest.param(".txt", 6),
        pytest.param(".py", 3),
    ],
)
def test_no_tokenizer(filled_tmp_dir, file_extension: str, expected_result: int):
    """
    Passes test if result without `tokenizer` is equal to `expected_result`.
    """
    assert universal_file_counter(filled_tmp_dir, file_extension) == expected_result


@pytest.mark.parametrize(
    ["file_extension", "expected_result"],
    [
        pytest.param("txt", 9),
        pytest.param("py", 0),
        pytest.param(".txt", 9),
        pytest.param(".py", 0),
    ],
)
def test_with_tokenizer(filled_tmp_dir, file_extension: str, expected_result: int):
    """
    Passes test if result with `str.split` `tokenizer` is equal to `expected_result`.
    """
    assert (
        universal_file_counter(filled_tmp_dir, file_extension, str.split)
        == expected_result
    )
