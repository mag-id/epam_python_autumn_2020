"""The entry point for `StocksParser` and data collecting."""

from json import dump, load
from parser import StocksParser  # pylint: disable=no-name-in-module
from pathlib import Path
from typing import Callable, Dict, List, Tuple

__all__ = ["main"]

CODE = "code"
NAME = "name"
PRICE = "price"
RATIO = "P/E"
GROWTH = "growth"
PROFIT = "potential profit"

ALL_DATA_STOCKS = "all_data_stocks.json"
TOP_TEN_EXPENSIVE_STOCKS = "top_ten_expensive_stocks.json"
TOP_TEN_LOW_RATIO_STOCKS = "top_ten_low_ratio_stocks.json"
TOP_TEN_GROWTHING_STOCKS = "top_ten_growthing_stocks.json"
TOP_TEN_PROFITING_STOCKS = "top_ten_profiting_stocks.json"


def main(path: str, encoding="UTF-8"):
    """
    Takes `path` to the save directory and:

    + Writes all parsed data by `StocksParser` to `all_data.json` file.

    Note:
    -----
    `top_ten_*` results sort in ascending order.

    + Writes top ten the most expensive stocks with prices in
    RUB to `top_ten_expensive_stocks.json` file in the format
    ```
    {"code": str, "name": str, "price" float}
    ```

    + Writes top ten the lowest P/E ratio stocks to
    `top_ten_low_ratio_stocks.json` file in the format
    ```
    {"code": str, "name": str, "P/E" float}
    ```

    + Writes top ten the most growing stocks at last year in
    percentage to `top_ten_growthing_stocks.json` file in the format
    ```
    {"code": str, "name": str, "growth" float}
    ```

    + Writes top ten the most potentially profiting stocks in
    percentage to `top_ten_profiting_stocks.json` file in the format
    ```
    {"code": str, "name": str, "potential profit" float}
    ```

    By default `encoding` is "UTF-8".
    """
    directory = Path(path)

    all_data_json = directory.joinpath(ALL_DATA_STOCKS)
    dump_as_json(StocksParser.execute(), all_data_json)

    with open(file=all_data_json, mode="r", encoding=encoding) as as_json:
        expensive, low_ratio, growthing, profiting = keep_top_tens(load(as_json))

    dump_as_json(expensive, directory.joinpath(TOP_TEN_EXPENSIVE_STOCKS))
    dump_as_json(low_ratio, directory.joinpath(TOP_TEN_LOW_RATIO_STOCKS))
    dump_as_json(growthing, directory.joinpath(TOP_TEN_GROWTHING_STOCKS))
    dump_as_json(profiting, directory.joinpath(TOP_TEN_PROFITING_STOCKS))


def dump_as_json(data: List[Dict], path: Path, encoding="UTF-8"):
    """
    Writes `data` to json file to `path`. By default `encoding` is "UTF-8".
    """
    with open(file=path, mode="w", encoding=encoding) as as_json:
        dump(data, as_json, indent=4)


def keep_top_tens(stocks: List[Dict]) -> Tuple[List[Dict]]:
    """
    Takes `stocks` and returns `Tuple` with four `List`s
    (sort in ascending order):

    + Top ten the most expensive stocks with prices
    in RUB in the format
    ```
    {"code": str, "name": str, "price" float}
    ```

    + Top ten the lowest P/E ratio stocks
    in the format
    ```
    {"code": str, "name": str, "P/E" float}
    ```

    + Top ten the most growing stocks at last year
    in percentage in the format
    ```
    {"code": str, "name": str, "growth" float}
    ```

    + Writes top ten the most potentially profiting stocks
    in percentage in the format
    ```
    {"code": str, "name": str, "potential profit" float}
    ```
    """
    expensive, low_ratio, growthing, profiting = [], [], [], []

    for stock in stocks:
        _filter_queue(PRICE, stock, expensive, lambda queue: min(queue, key=_key_price))
        if stock[RATIO]:
            _filter_queue(
                RATIO, stock, low_ratio, lambda queue: max(queue, key=_key_ratio)
            )
        _filter_queue(
            GROWTH, stock, growthing, lambda queue: min(queue, key=_key_growth)
        )
        _filter_queue(
            PROFIT, stock, profiting, lambda queue: min(queue, key=_key_profit)
        )

    expensive.sort(key=_key_price)
    low_ratio.sort(key=_key_ratio)
    growthing.sort(key=_key_growth)
    profiting.sort(key=_key_profit)

    return expensive, low_ratio, growthing, profiting


def _filter_queue(key: str, stock: Dict, queue: List, remove_filter: Callable):
    """
    Adds key-value from `stock` according to `key`.
    Maintains `queue` according to `filter_` invariant.

    Arguments:
    + `key` - necessary key for `stock`.
    + `stock` - current stock entry.
    + `queue` - a list which keeps queue with length 10 according to `filter_`.
    + `remove_filter` - function which keeps queue invariant.
    """
    queue.append({CODE: stock[CODE], NAME: stock[NAME], key: stock[key]})
    if len(queue) > 10:
        queue.remove(remove_filter(queue))


def _key_price(stock: Dict) -> float:
    """
    Returns value from `stock` for `PRICE` key.
    """
    return stock[PRICE]


def _key_ratio(stock: Dict) -> float:
    """
    Returns value from `stock` for `RATIO` key.
    """
    return stock[RATIO]


def _key_growth(stock: Dict) -> float:
    """
    Returns value from `stock` for `GROWTH` key.
    """
    return stock[GROWTH]


def _key_profit(stock: Dict) -> float:
    """
    Returns value from `stock` for `PROFIT` key.
    """
    return stock[PROFIT]


if __name__ == "__main__":
    main("homework_10")
