"""
Unit tests for module `homework_4.tasks.task_1`.
"""

# pylint: disable=redefined-outer-name

from tempfile import NamedTemporaryFile

import pytest

from homework_4.tasks.task_1 import NOT_EXIST, NOT_READABLE, read_magic_number


@pytest.fixture()
def no_permissions_path(tmp_path):
    """
    Returns temporary path without permissions.
    """
    path = tmp_path / "tmp_dir"
    path.mkdir(mode=0000)
    return path


def test_negative_not_readeble_case_read_magic_number(no_permissions_path):
    """
    Passes test if `ValueError` with `NOT_READABLE` message raises.
    """
    with pytest.raises(ValueError) as exception_info:
        read_magic_number(no_permissions_path)
    assert str(exception_info.value) == NOT_READABLE


def test_negative_not_exist_case_read_magic_number():
    """
    Passes test if `ValueError` with `NOT_EXIST` message raises.
    """
    with NamedTemporaryFile(mode="tr") as temporary:
        path = temporary.name

    with pytest.raises(ValueError) as exception_info:
        read_magic_number(path)

    assert str(exception_info.value) == NOT_EXIST


@pytest.mark.parametrize(
    ["content", "expected_result"],
    [
        pytest.param("-1\n4\n", False, id="False: first line is -1."),
        pytest.param("0\n4\n", False, id="False: first line is 0."),
        pytest.param("1\n4\n", True, id="True: first line is 1."),
        pytest.param("2\n4\n", True, id="True: first line is 2."),
        pytest.param("3\n4\n", False, id="False: first line is 3."),
        pytest.param("4\n4\n", False, id="False: first line is 4."),
    ],
)
def test_positive_cases_integers_read_magic_number(content, expected_result):
    """
    Passes test if result of `read_magic_number` under  `file.name`
    path with `content` is equal with `expected_result`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name) == expected_result


@pytest.mark.parametrize(
    ["content", "expected_result"],
    [
        pytest.param("-1.0\n4\n", False, id="False: first line is -1.0."),
        pytest.param("0.99999\n4\n", False, id="False: first line is 0.99999"),
        pytest.param("1.0\n4\n", True, id="True: first line is 1.0."),
        pytest.param("2.0\n4\n", True, id="True: first line is 2.0."),
        pytest.param("2.99999\n4\n", True, id="True: first line is 2.99999."),
        pytest.param("3.0\n4\n", False, id="False: first line is 3.0."),
    ],
)
def test_positive_cases_dots_read_magic_number(content, expected_result):
    """
    Passes test if result of `read_magic_number` under  `file.name`
    path with `content` is equal with `expected_result`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name) == expected_result


@pytest.mark.parametrize(
    ["content", "expected_result"],
    [
        pytest.param("-1,0\n4\n", False, id="False: first line is -1,0."),
        pytest.param("0,99999\n4\n", False, id="False: first line is 0,99999"),
        pytest.param("1,0\n4\n", True, id="True: first line is 1,0."),
        pytest.param("2,0\n4\n", True, id="True: first line is 2,0."),
        pytest.param("2,99999\n4\n", True, id="True: first line is 2,99999."),
        pytest.param("3,0\n4\n", False, id="False: first line is 3,0."),
    ],
)
def test_positive_cases_commas_read_magic_number(content, expected_result):
    """
    Passes test if result of `read_magic_number` under  `file.name`
    path with `content` is equal with `expected_result`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name) == expected_result


@pytest.mark.parametrize(
    ["content", "expected_result"],
    [
        pytest.param("string\n4\n", False, id="False: first line is string."),
        pytest.param("True\n4\n", False, id="False: first line is True."),
        pytest.param("", False, id="False: no content."),
    ],
)
def test_boundary_cases_read_magic_number(content, expected_result):
    """
    Passes test if result of `read_magic_number` under  `file.name`
    path with `content` is equal with `expected_result`.
    """
    with NamedTemporaryFile(mode="tw", encoding="utf-8") as file:
        file.write(content)
        file.seek(0)
        assert read_magic_number(file.name) == expected_result
