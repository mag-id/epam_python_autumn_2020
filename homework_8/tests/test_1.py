"""Unit tests for module `homework_8.tasks.task_1`."""

from tempfile import NamedTemporaryFile
from typing import Any, Dict

import pytest

from homework_8.tasks.task_1 import (
    INVALID_KEY,
    INVALID_PAIR,
    KeyValueStorage,
    _check,
    _parse,
)

ENCODING = "UTF-8"
SEPARATOR = "="

SIMPLE_CASE = "name=kek\nlast_name=top\npower=9001\nsong=shadilay"
SIMPLE_CASE_RESULT = {
    "name": "kek",
    "last_name": "top",
    "power": 9001,
    "song": "shadilay",
}


# pylint: disable=redefined-outer-name
@pytest.fixture()
def simple_case_filepath(tmp_path):
    """
    Returns temporary file path to file with
    `SIMPLE_CASE` and `ENCODING` encoding.
    """
    test_dir = tmp_path / "tmp_dir"
    test_dir.mkdir()
    test_data = test_dir / "simple_case.txt"
    test_data.write_text(SIMPLE_CASE, encoding=ENCODING)
    return test_data


class TestCheck:
    """Wraps tests for `_check`."""

    @staticmethod
    @pytest.mark.parametrize(
        ["key"],
        [
            pytest.param("valid_string", id="'valid_string'"),
            pytest.param("_0123", id="'_0123'"),
            pytest.param("valid_0123", id="'valid_0123'"),
            pytest.param("_0123valid", id="'_0123valid'"),
        ],
    )
    def test_key_true(key: Any):
        """Passes test if `_check` result is `True` for valid `key`."""
        assert _check(key)

    @staticmethod
    @pytest.mark.parametrize(
        ["key"],
        [
            # Empty strings and bracets.
            pytest.param("", id="''"),
            pytest.param(" ", id="' '"),
            pytest.param("'", id="'"),
            pytest.param("''", id="''''"),
            pytest.param("' '", id="'' ''"),
            pytest.param("{", id="'{'"),
            pytest.param("{}", id="'{}'"),
            pytest.param("([{}])", id="'([{}])'"),
            # Dots, commas, and other characters.
            pytest.param(".", id="'.'"),
            pytest.param("..", id="'..'"),
            pytest.param("...", id="'...'"),
            pytest.param("|", id="|"),
            pytest.param("/", id="'/'"),
            pytest.param(":", id="':'"),
            # Work characters.
            pytest.param("\\", id="'\\'"),
            pytest.param("\n", id="'\\n'"),
            pytest.param("\t", id="'\\t'"),
            pytest.param("\b", id="'\\b'"),
            # Space separated and combinated cases.
            pytest.param("0123", id="'0123'"),
            pytest.param("inv@lid", id="'inv@lid'"),
            pytest.param("invalid 0123", id="'invalid 0123'"),
            pytest.param("invalid-0123", id="'invalid-0123'"),
            pytest.param("invalid\t0123", id="'invalid\\t0123'"),
            pytest.param("invalid\\t0123", id="'invalid\\\t0123'"),
        ],
    )
    def test_key_false(key: Any):
        """Passes test if `_check` result is `False` for invalid `key`."""
        assert _check(key) is False


class TestParse:
    """Wraps tests for `_parse`."""

    @staticmethod
    def test_empty():
        """Passes test if `_parse` returns empty dictionary from an empty file."""
        with NamedTemporaryFile(mode="wt") as file:
            file.write("")
            file.seek(0)
            assert _parse(path=file.name, separator=SEPARATOR, encoding=ENCODING) == {}

    @staticmethod
    @pytest.mark.parametrize(
        ["file_content"],
        [
            pytest.param("\n", id="'\n'"),
            pytest.param("\n\n", id="'\n\n'"),
            pytest.param("\n\n\n", id="'\n\n\n'"),
            pytest.param("key=True\n==False", id="'key=True\n==False'"),
        ],
    )
    def test_invalid_pair(file_content: str):
        """Passes test if `_parse` raises `ValueError(INVALID_PAIR)`."""
        with NamedTemporaryFile(mode="wt") as file:
            file.write(file_content)
            file.seek(0)
            with pytest.raises(ValueError, match=INVALID_PAIR):
                _parse(path=file.name, separator=SEPARATOR, encoding=ENCODING)

    @staticmethod
    @pytest.mark.parametrize(
        ["file_content"],
        [
            pytest.param("key=True\n=False", id="'key=True\n=False'"),
            pytest.param("key=True\n0=False", id="'key=True\n0=False'"),
            pytest.param("key=True\ninv@lid=False", id="'key=True\ninv@lid=False'"),
        ],
    )
    def test_invalid_key(file_content: str):
        """Passes test if `_parse` raises `ValueError(INVALID_KEY)`."""
        with NamedTemporaryFile(mode="wt") as file:
            file.write(file_content)
            file.seek(0)
            with pytest.raises(ValueError, match=INVALID_KEY):
                _parse(path=file.name, separator=SEPARATOR, encoding=ENCODING)

    @staticmethod
    @pytest.mark.parametrize(
        ["file_content", "expected_result"],
        [
            pytest.param(
                "key=True\nvalid=True",
                {"key": "True", "valid": "True"},
                id="'key=True\nvalid=True'",
            ),
            pytest.param(
                "key=True\n_0=True",
                {"key": "True", "_0": "True"},
                id="'key=True\n_0=True'",
            ),
        ],
    )
    def test_expected_result(file_content: str, expected_result: Dict[str, int or str]):
        """Passes test if `_parse` result is equal to `expected_result`."""
        with NamedTemporaryFile(mode="wt") as file:
            file.write(file_content)
            file.seek(0)
            assert (
                _parse(path=file.name, separator=SEPARATOR, encoding=ENCODING)
                == expected_result
            )


class TestKeyValueStorage:
    """Wraps tests for `TestKeyValueStorage`."""

    @staticmethod
    def test_attribute_access(simple_case_filepath):
        """
        Passes test if `KeyValueStorage` initialization is successful and
        `instance.key == value` and `instance[key] == value` behaviour is correct.
        """
        instance = KeyValueStorage(simple_case_filepath)

        assert instance["name"] == "kek"
        assert instance.name == "kek"

        assert instance["power"] == 9001
        assert instance.power == 9001

    @staticmethod
    def test_value_reassignment(simple_case_filepath):
        """
        Passes test if `KeyValueStorage` `instance` raises
        `TypeError: 'KeyValueStorage' object does not support item assignment`
        during value reassignment.
        """
        instance = KeyValueStorage(simple_case_filepath)
        with pytest.raises(
            TypeError, match="'KeyValueStorage' object does not support item assignment"
        ):
            instance["name"] = "new kek"

    @staticmethod
    def test_attribute_reassignment(simple_case_filepath):
        """
        Passes test if `KeyValueStorage` `instance` raises
        `TypeError: 'KeyValueStorage' object does not support item assignment`
        during attribute reassignment.
        """
        instance = KeyValueStorage(simple_case_filepath)
        with pytest.raises(
            TypeError, match="'KeyValueStorage' object does not support item assignment"
        ):
            instance.name = "new kek"

    @staticmethod
    def test_new_key_value_assignment(simple_case_filepath):
        """
        Passes test if `KeyValueStorage` `instance` raises
        `TypeError: 'KeyValueStorage' object does not support item assignment`
        during new key-value assignment.
        """
        instance = KeyValueStorage(simple_case_filepath)
        with pytest.raises(
            TypeError, match="'KeyValueStorage' object does not support item assignment"
        ):
            instance["new_name"] = "new kek"

    @staticmethod
    def test_new_attribute_assignment(simple_case_filepath):
        """
        Passes test if `KeyValueStorage` `instance` raises
        `TypeError: 'KeyValueStorage' object does not support item assignment`
        during new attribute assignment.
        """
        instance = KeyValueStorage(simple_case_filepath)
        with pytest.raises(
            TypeError, match="'KeyValueStorage' object does not support item assignment"
        ):
            instance.new_name = "new kek"
