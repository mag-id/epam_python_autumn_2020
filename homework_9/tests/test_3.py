"""
Unit tests for `universal_file_counter`
from module `homework_9.tasks.task_3`.
"""

from pathlib import Path

import pytest

from homework_9.tasks.task_3 import universal_file_counter

# pylint: disable=redefined-outer-name


@pytest.fixture
def tmp_dir(tmp_path) -> Path:
    """
    Returns `Path` to the temporary directory.
    If It not exists - creates and returns it.
    """
    dir_path = tmp_path / "tmp_dir"
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


# https://stackoverflow.com/questions/44677426
@pytest.fixture
def create_tmp_file(tmp_dir) -> Path:
    """
    Writes file at `tmp_dir` with given `name` and `content`.

    Arguments:
    ----------
    + `name` - name of the `tmp_file`, `str`.
    + `content` - content of the `tmp_file`, `str`.

    Returns:
    --------
    + `tmp_file` - `Path` to the temporary file.
    """

    def tmp_file(name: str, content: str) -> Path:
        """
        File `Path` from `create_tmp_file`
        fixture with given `name` and `content`.
        """
        file = tmp_dir / name
        file.write_text(content)
        return file

    return tmp_file


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
