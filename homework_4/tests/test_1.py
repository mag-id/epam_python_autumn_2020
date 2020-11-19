"""
Unit tests for module `homework_4.tasks.task_1`.
"""
from tempfile import NamedTemporaryFile

import pytest

from homework_4.tasks.task_1 import NOT_EXIST, NOT_READABLE, read_magic_number


@pytest.fixture()
def no_permissions_file_path(tmp_path):
    """
    Returns temporary file path without permissions.
    """
    file_path = tmp_path / "tmp_dir"
    file_path.mkdir(mode=0000)
    yield file_path
    file_path.rmdir()


# pylint: disable=redefined-outer-name
def test_negative_not_readeble_case_for_read_magic_number(no_permissions_file_path):
    """
    Passes test if `ValueError` with `NOT_READABLE` message raises.
    """
    with pytest.raises(ValueError, match=NOT_READABLE):
        read_magic_number(no_permissions_file_path)


def test_negative_not_exist_case_for_read_magic_number():
    """
    Passes test if `ValueError` with `NOT_EXIST` message raises.
    """
    with NamedTemporaryFile(mode="tr") as temporary:
        path = temporary.name

    with pytest.raises(ValueError, match=NOT_EXIST):
        read_magic_number(path)


@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        pytest.param("1\n4\n", id="True: first line is 1."),
        pytest.param("2\n4\n", id="True: first line is 2."),
    ],
)
def test_common_true_integers_cases_for_read_magic_number(content):
    """
    Passes test if result of `read_magic_number` under `file.name` path with `content` is `True`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name)


@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        pytest.param("1.0\n4\n", id="True: first line is 1.0."),
        pytest.param("2.0\n4\n", id="True: first line is 2.0."),
        pytest.param("2.99999\n4\n", id="True: first line is 2.99999."),
    ],
)
def test_common_true_dot_floats_cases_for_read_magic_number(content):
    """
    Passes test if result of `read_magic_number` under `file.name` path with `content` is `True`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name)


@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        pytest.param("1,0\n4\n", id="True: first line is 1,0."),
        pytest.param("2,0\n4\n", id="True: first line is 2,0."),
        pytest.param("2,99999\n4\n", id="True: first line is 2,99999."),
    ],
)
def test_common_true_comma_floats_cases_for_read_magic_number(content):
    """
    Passes test if result of `read_magic_number` under `file.name` path with `content` is `True`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name)


@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        pytest.param("-1\n4\n", id="False: first line is -1."),
        pytest.param("0\n4\n", id="False: first line is 0."),
        pytest.param("3\n4\n", id="False: first line is 3."),
        pytest.param("4\n4\n", id="False: first line is 4."),
    ],
)
def test_common_false_integers_cases_for_read_magic_number(content):
    """
    Passes test if result of `read_magic_number` under `file.name` path with `content` is `False`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name) is False


@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        pytest.param("-1.0\n4\n", id="False: first line is -1.0."),
        pytest.param("0.99999\n4\n", id="False: first line is 0.99999"),
        pytest.param("3.0\n4\n", id="False: first line is 3.0."),
    ],
)
def test_common_false_dot_floats_cases_for_read_magic_number(content):
    """
    Passes test if result of `read_magic_number` under `file.name` path with `content` is `False`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name) is False


@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        pytest.param("-1,0\n4\n", id="False: first line is -1,0."),
        pytest.param("0,99999\n4\n", id="False: first line is 0,99999"),
        pytest.param("3,0\n4\n", id="False: first line is 3,0."),
    ],
)
def test_common_false_comma_floats_cases_for_read_magic_number(content):
    """
    Passes test if result of `read_magic_number` under `file.name` path with `content` is `False`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name) is False


@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        pytest.param("string\n4\n", id="False: first line is string."),
        pytest.param("", id="False: no content."),
    ],
)
def test_other_false_cases_for_read_magic_number(content):
    """
    Passes test if result of `read_magic_number` under `file.name` path with `content` is `False`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name) is False
