"""Pytest fixtures for `homework_9.tests.test_1` and `homework_9.tests.test_3`"""

from pathlib import Path

import pytest

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
