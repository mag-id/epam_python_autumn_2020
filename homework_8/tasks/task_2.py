"""
Task 2
======

Write a wrapper class `TableData` for database table,
that when initialized with database name and table acts as collection object
(implements Collection protocol).

Assume all data has unique values in `name` column. So, if
```
presidents = TableData(database_name="example.sqlite", table_name="presidents")
```

then
+ `len(presidents)` will give current amount of rows in presidents table in database
+ `presidents["Yeltsin"]` should return
single data row for president with name `"Yeltsin"`
+ `"'Yeltsin' in presidents"` should return if president with same name exists in table
+ object implements iteration protocol. i.e. you could use it in for loops:
```
for president in presidents:
    print(president["name"])
```

+ all above mentioned calls should reflect most recent data.
If data in table changed after you created collection instance,
your calls should return updated data.

Avoid reading entire table into memory.
When iterating through records, start reading the first record,
then go to the next one, until records are exhausted.

When writing tests, it's not always neccessary to mock database calls completely.
Use supplied `example.sqlite` file as database fixture file.


About `example.sqlite`
======================

We have a database file (`example.sqlite`) in sqlite3 format with some tables and data.
All tables have `name` column and maybe some additional ones.

Data retrieval and modifications are done with sqlite3 module by issuing SQL statements.
For example, to get all data from `TABLE1`:
```
import sqlite3
conn = sqlite3.connect("example.db")
cursor = conn.cursor()
cursor.execute("SELECT * from TABLE1")
data = cursor.fetchall()   # will be a list with data.
```

instead of getting all data at once,
you can use `.fetchone()` calls and named expressions:
```
while row:=cursor.fetchone():
    print(row)
```

To get a row with specific name equal to some value:
```
import sqlite3
conn = sqlite3.connect("example.db")
cursor = conn.cursor()
cursor.execute("SELECT * from presidents where name=:name", {name:"Yeltsin"})
data = cursor.fetchall()  # will get all records with this name.
# You can also use .fetchone() to get one record.
```

in order to get record with first name (sorted alphabetically) use SQL expression
`SELECT * from presidents order by name asc limit 1`,
in order to get record after specified (sorted alphabetically) use SQL expression
`SELECT * from presidents where name > :name order by name limit`.

To get amount of records in table `TABLE1`, use `select count(*) from TABLE1` query.

Please refer to this documents for more information
about how to retrieve data from sqlite database:
+ [DBAPI](https://www.python.org/dev/peps/pep-0249/)
+ [sqlite3 module](https://docs.python.org/3/library/sqlite3.html).
"""
from sqlite3 import Cursor, connect
from typing import Any, Dict, Iterator, Tuple


class _Table:
    """
    Connects to the database table with `table_name`
    and `primary_key` at the `database_name` path.

    Properties:
    -----------
    + `database_name` - returns `database_name`.
    + `table_name` - returns `table_name`.
    + `primary_key` - returns `primary_key`.

    Methods:
    --------
    + `get_column_names` - returns column names of the table.
    + `get_cursor` - takes `sql_expression`, returns `sqlite3.Cursor` instance.
    """

    def __init__(self, database_name: str, table_name: str, primary_key: str):
        self.__database_name = database_name
        self.__table_name = table_name
        self.__primary_key = primary_key

    @property
    def database_name(self) -> str:
        """Returns `database_name`."""
        return self.__database_name

    @property
    def table_name(self) -> str:
        """Returns `table_name`."""
        return self.__table_name

    @property
    def primary_key(self) -> str:
        """Returns `primary_key`."""
        return self.__primary_key

    # https://stackoverflow.com/questions/5010042
    def get_column_names(self) -> Tuple[str]:
        """Returns column names of the table."""
        cursor = self.get_cursor(f"SELECT * FROM {self.table_name} LIMIT 1")
        return tuple(map(lambda raw_: raw_[0], cursor.description))

    def get_cursor(self, sql_expression: str) -> Cursor:
        """
        Returns `sqlite3.Cursor` instance
        with result of the `sql_expression`.
        """
        with connect(self.database_name) as cursor:
            return cursor.execute(sql_expression)


class _TableIter:
    """Takes `table` and implements iterator protocol."""

    def __init__(self, table: _Table):
        self.__rows_cursor = table.get_cursor(f"SELECT * FROM {table.table_name}")
        self.__column_names = table.get_column_names()

    def __iter__(self) -> "TableIter":
        return self

    def __next__(self) -> Dict:
        if row := self.__rows_cursor.fetchone():
            return dict(zip(self.__column_names, row))
        raise StopIteration


class TableData:
    """
    Connects to the database table with `table_name` at the `database_name` path.
    Implements collection protocol and iterator protocol.

    Example:
    --------
    ```

    >>> table = TableData("homework_8/tasks/example.sqlite", "presidents")

    >>> assert len(table) == 3

    # table["Noname"] - raises KeyError("Noname")
    >>> assert table["Yeltsin"] == {"name": "Yeltsin", "age": 999, "country": "Russia"}

    >>> assert "Yeltsin" in table
    >>> assert "Noname" not in table

    >>> assert list(table)[0]=={"name":"Yeltsin","age":999,"country":"Russia"}
    >>> assert list(table)[1]=={"name":"Trump","age":1337,"country":"US"}
    >>> assert list(table)[2]=={"name":"Big Man Tyrone","age":101,"country":"Kekistan"}

    ```
    """

    # https://stackoverflow.com/questions/37329370
    def __init__(self, database_name: str, table_name: str):
        self.__table = _Table(database_name, table_name, "name")

    # Method 2 from https://stackoverflow.com/questions/4253960
    def __contains__(self, identifier: Any) -> bool:
        cursor = self.__table.get_cursor(
            f"""
            SELECT COUNT(1) FROM {self.__table.table_name}
            WHERE {self.__table.primary_key}='{identifier}'
            """
        )
        return bool(*cursor.fetchone())

    def __getitem__(self, identifier: Any) -> Dict:
        cursor = self.__table.get_cursor(
            f"""
            SELECT * FROM {self.__table.table_name}
            WHERE {self.__table.primary_key}='{identifier}'
            """
        )
        if row := cursor.fetchone():
            return dict(zip(self.__table.get_column_names(), row))
        raise KeyError(identifier)

    def __len__(self) -> int:
        cursor = self.__table.get_cursor(
            f"SELECT COUNT(*) FROM {self.__table.table_name}"
        )
        return int(*cursor.fetchone())

    def __iter__(self) -> Iterator[Dict]:
        return _TableIter(self.__table)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
