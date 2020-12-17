"""Unit tests for module `homework_8.tasks.task_2`."""

from sqlite3 import connect
from typing import Any

import pytest

from homework_8.tasks.task_2 import TableData, _Table, _TableIter

TABLE = "presidents"
PRIMARY_KEY = "name"
COLUMN_NAMES = "name", "age", "country"

RECORDS = [
    {"name": "Yeltsin", "age": 999, "country": "Russia"},
    {"name": "Trump", "age": 1337, "country": "US"},
    {"name": "Big Man Tyrone", "age": 101, "country": "Kekistan"},
]
NEW_RECORD = {"name": "NoName", "age": 0, "country": "NoCountry"}
INSERT_NEW = "INSERT INTO presidents VALUES('NoName', 0, 'NoCountry')"


# pylint: disable=redefined-outer-name
@pytest.fixture
def setup_database(tmp_path):
    """
    Retruns path to the `database.sqlite` in the temporary direcory which
    contains `TABLE` with `PRIMARY_KEY` and `RECORDS` with `COLUMN_NAMES`.
    """
    test_dir = tmp_path / "tmp_dir"
    test_dir.mkdir()
    database_name = test_dir / "database.sqlite"

    with connect(database_name) as cursor:
        cursor.execute(
            """
            CREATE TABLE presidents (
                name text PRIMARY KEY,
                age integer,
                country text
            )
            """
        )
        cursor.executemany(
            "INSERT INTO presidents VALUES(?, ?, ?)",
            [tuple(record.values()) for record in RECORDS],
        )
    return database_name


class TestTable:
    """Wraps `_Table` tests."""

    @staticmethod
    def test_attributes(setup_database):
        """
        Passes test if `_Table` `instance` saves
        attributes with which it was initialized.
        """
        instance = _Table(setup_database, TABLE, PRIMARY_KEY)
        assert (
            instance.database_name == setup_database
        )  # pylint: disable=comparison-with-callable
        assert instance.table_name == TABLE
        assert instance.primary_key == PRIMARY_KEY

    @staticmethod
    def test_assertion_error(setup_database):
        """
        Passes test if `_Table` `instance` attributes are not
        accesseble for resetting and raises `AttributeError`.
        """
        instance = _Table(setup_database, TABLE, PRIMARY_KEY)

        with pytest.raises(AttributeError):
            instance.database_name = "new value"

        with pytest.raises(AttributeError):
            instance.table_name = "new value"

        with pytest.raises(AttributeError):
            instance.primary_key = "new value"

    @staticmethod
    def test_get_column_names(setup_database):
        """
        Passes test if `get_column_names()` method of the
        `_Table` `instance` returns valid column names.
        """
        instance = _Table(setup_database, TABLE, PRIMARY_KEY)
        assert instance.get_column_names() == COLUMN_NAMES

    @staticmethod
    @pytest.mark.parametrize(
        ["sql_expression", "expected_result"],
        [
            pytest.param(
                f"SELECT * FROM {TABLE}",
                [tuple(record.values()) for record in RECORDS],
                id="List of tuples with record values for earch record in RECORDS",
            ),
            pytest.param(
                f"SELECT COUNT(*) FROM {TABLE}",
                [(3,)],
                id="f'COUNT(*) FROM {TABLE}' returns [(3,)]",
            ),
            pytest.param(
                f"""
                SELECT * FROM {TABLE}
                WHERE {PRIMARY_KEY}='{RECORDS[0]["name"]}'
                """,
                [tuple(RECORDS[0].values())],
                id="[('Yeltsin', 999, 'Russia')]",
            ),
        ],
    )
    def test_get_cursor(setup_database, sql_expression: str, expected_result: Any):
        """
        Passes test if `get_cursor(sql_expression).fetchall()`
        of the `_Table` `instance` returns `expected_result`.
        """
        instance = _Table(setup_database, TABLE, PRIMARY_KEY)
        assert instance.get_cursor(sql_expression).fetchall() == expected_result


class TestTableIter:
    """Wraps `_TableIter` tests."""

    @staticmethod
    def test_next(setup_database):
        """
        Passes test if `next()` and `__next__()` on the
        `_TableIter` `instance` returns correct results.
        """
        instance = _TableIter(_Table(setup_database, TABLE, PRIMARY_KEY))

        first = next(instance)
        second = instance.__next__()
        third = instance.__next__

        assert [first, second, third()] == RECORDS

    @staticmethod
    def test_next_stop_iteration(setup_database):
        """
        Passes test if extra `next()` call on the
        `_TableIter` `instance` raises `StopIteration`.
        """
        instance = _TableIter(_Table(setup_database, TABLE, PRIMARY_KEY))

        next(instance)
        next(instance)
        next(instance)

        with pytest.raises(StopIteration):
            next(instance)

    @staticmethod
    def test_iter(setup_database):
        """
        Passes test if `__iter__()` call on the
        `_TableIter` `instance` returns themself.
        """
        instance = _TableIter(_Table(setup_database, TABLE, PRIMARY_KEY))
        assert isinstance(instance.__iter__(), _TableIter)


class TestTableData:
    """Wraps `TableData` tests."""

    @staticmethod
    def test_contains_true(setup_database):
        """
        Passes test if `TableData` `instance` contains "Trump"
        """
        instance = TableData(setup_database, TABLE)
        assert instance.__contains__("Trump")
        assert "Trump" in instance

    @staticmethod
    def test_contains_false(setup_database):
        """
        Passes test if `TableData` `instance` not contains "NoName"
        """
        instance = TableData(setup_database, TABLE)
        assert instance.__contains__("NoName") is False
        assert ("NoName" in instance) is False
        assert "NoName" not in instance

    @staticmethod
    def test_getitem(setup_database):
        """
        Passes test if attempting to get the "Trump"
        record from `TableData` `instance` is valid.
        """
        instance = TableData(setup_database, TABLE)
        president = "Trump"
        assert instance.__getitem__(president) == RECORDS[1]
        assert instance[president] == RECORDS[1]

    @staticmethod
    def test_getitem_key_error(setup_database):
        """
        Passes test if attempting to get the "NoName" record
        from `TableData` `instance` raises `KeyError("NoName")`.
        """
        instance = TableData(setup_database, TABLE)
        president = "NoName"

        with pytest.raises(KeyError, match=president):
            _ = instance.__getitem__(president)

        with pytest.raises(KeyError, match=president):
            _ = instance[president]

    @staticmethod
    def test_len(setup_database):
        """
        Passes test if the `len()` of the `TableData`
        `instance` is equal to the `len(RECORDS)`.
        """
        instance = TableData(setup_database, TABLE)
        assert instance.__len__() == len(RECORDS)
        assert len(instance) == len(RECORDS)

    @staticmethod
    def test_iter(setup_database):
        """
        Passes test if `__iter__()` call on the
        `TableData` `instance` returns `_TableIter` instance.
        """
        instance = TableData(setup_database, TABLE)
        assert isinstance(instance.__iter__(), _TableIter)


class TestTableDataDynamicChanges:
    """Wraps `TableData` tests during dynamic database changes."""

    @staticmethod
    def test_contains(setup_database):
        """
        Passes test if "NoName" record (`NEW_RECORD`)
        not in `TableData` `instance` before explisit
        `NEW_RECORD` injection (`INSERT_NEW`), and in
        `TableData` `instance` after,
        without `TableData` `instance` recreating.
        """
        instance = TableData(setup_database, TABLE)
        assert "NoName" not in instance

        with connect(setup_database) as cursor:
            cursor.execute(INSERT_NEW)
        assert "NoName" in instance

    @staticmethod
    def test_getitem(setup_database):
        """
        Passes test if atteption to get "NoName" record (`NEW_RECORD`)
        from `TableData` `instance` raises `KeyError(NoName)` before
        explisit `NEW_RECORD` injection (`INSERT_NEW`), and seccessful
        after, without `TableData` `instance` recreating.
        """
        instance = TableData(setup_database, TABLE)

        with pytest.raises(KeyError, match="NoName"):
            _ = instance["NoName"]

        with connect(setup_database) as cursor:
            cursor.execute(INSERT_NEW)
        assert instance["NoName"] == NEW_RECORD

    @staticmethod
    def test_len(setup_database):
        """
        Passes test if `len()` of the `TableData` `instance` before
        explisit `NEW_RECORD` injection (`INSERT_NEW`) is equal to 3,
        and and equal to 4 after, without `TableData` `instance` recreating.
        """
        instance = TableData(setup_database, TABLE)

        assert len(instance) == 3

        with connect(setup_database) as cursor:
            cursor.execute(INSERT_NEW)
        assert len(instance) == 4
