"""`StocksParser` realization via `Parser` from `stocks.interface`."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from json import dump
from queue import PriorityQueue
from typing import Dict, Iterator, List

from functions import (
    collect_stocks_growths,
    get_pagination_hyperlinks,
    get_stock,
    get_stocks_hyperlinks,
    get_stocks_table,
)
from interface import Parser

__all__ = ["StocksParser"]

MESSAGE = "`queue_cache` must be > 0."


class AutoPriorityQueue(PriorityQueue):
    """
    `PriorityQueue` with `auto_put` method.
    """

    def auto_put(self, item, block=True, timeout=None):
        """
        Works like `PriorityQueue.put`, but if a queue is full hight
        priority item will be removed and a new item will be put into a queue.
        """
        if self.full():
            self.get()
        self.put(item, block=block, timeout=timeout)


class StocksParser:
    """
    `Parser` realization for
    `https://markets.businessinsider.com/index/components/s&p_500`.

    Collect for each stock next data from [S&P 500
    ](https://en.wikipedia.org/wiki/S%26P_500_Index) list:

    + "name" - Stock name, `str`.

    + "code" - Stock code, `str`.

    + "growth" - Stock year growth, `float` percentages.

    + "price" - Stock price in RUB according to USD-RUB [daily quotation
    ](http://www.cbr.ru/scripts/XML_daily.asp)
    according to [The Central Bank of the Russian Federation
    ](http://www.cbr.ru/development/sxml/), `float` RUB.

    + "ratio" - [Price-earnings (P/E) ratio
    ](https://en.wikipedia.org/wiki/Price–earnings_ratio)
    of a stock, `float`. If not found - returns `False`.

    + "profit" - potential profit, the difference between [Week High 52 and Week Low 52
    ](https://www.investopedia.com/terms/1/52weekhighlow.asp), `float` percentages.

    Note:
    -----
    `price` and `potential profit` round to the hundredths.

    Default key-value arguments:
    ----------------------------
    + `queue_cache` - Number of stocks to write. `10` by default.
    + `max_workers` - Max number of threads for pages parsing.
    `None` by default i.e. number of pagination pages.
    + `print_stock` - Prints whole raw stock info in StdOut.
    `False` by default.
    """

    __site, __entry = "https://markets.businessinsider.com", "/index/components/s&p_500"

    def __init__(
        self, queue_cache: int = 10, max_workers: int = None, print_stock: bool = False
    ):
        self.__max_workers = max_workers
        self.__print_stock = print_stock

        if queue_cache > 0:
            self.__queue_cache = queue_cache + 1
        else:
            raise ValueError(MESSAGE)

        self.__expensive = AutoPriorityQueue(self.__queue_cache)
        self.__low_ratio = AutoPriorityQueue(self.__queue_cache)
        self.__growthing = AutoPriorityQueue(self.__queue_cache)
        self.__profiting = AutoPriorityQueue(self.__queue_cache)

    def execute(self):
        """
        Starts parsing.
        """
        pages = self.__get_pages()
        with ThreadPoolExecutor(self.__max_workers or len(pages)) as executor:
            executor.map(self.__update, pages)

    def dump_low_ratio(self, path: str, encoding="UTF-8"):
        """
        Saves to `path` as JSON top of the lowest P/E
        ratio stocks. By default `encoding` = `"UTF-8"`.

        Format:
        -------
        ```
        [{"ratio" float, "name": str, "code": str}]
        ```
        """

        def helper(priority_stockratio_pair) -> "StockRatio":
            """Helps to get `StockRatio` container as dictionary."""
            return asdict(priority_stockratio_pair[-1])

        return self.__dump_as_json(
            list(map(helper, sorted(self.__low_ratio.queue)))[1:],
            path,
            encoding=encoding,
        )

    def dump_expensive(self, path: str, encoding="UTF-8"):
        """
        Saves to `path` as JSON top of the most expensive stocks with prices
        in RUB rounded to the hundredths. By default `encoding` = `"UTF-8"`.

        Format:
        -------
        ```
        [{"price" float, "name": str, "code": str}]
        ```
        """
        return self.__dump_as_json(
            list(map(asdict, sorted(self.__expensive.queue)))[1:],
            path,
            encoding=encoding,
        )

    def dump_growthing(self, path: str, encoding="UTF-8"):
        """
        Saves to `path` as JSON top of the most growing stocks at
        last year in percentage. By default `encoding` = `"UTF-8"`.

        Format:
        -------
        ```
        [{"growth" float, "name": str, "code": str}]
        ```
        """
        return self.__dump_as_json(
            list(map(asdict, sorted(self.__growthing.queue)))[1:],
            path,
            encoding=encoding,
        )

    def dump_profiting(self, path, encoding="UTF-8"):
        """
        Saves to `path` as JSON top of the most potentially profiting stocks in
        percentage rounded to the hundredths. By default `encoding` = `"UTF-8"`.

        Formula:
        --------
        `potential profit` = (100% * 52 Week High) / 52 Week Low - 100%.

        Format:
        -------
        ```
        [{"profit" float, "name": str, "code": str}]
        ```
        """
        return self.__dump_as_json(
            list(map(asdict, sorted(self.__profiting.queue)))[1:],
            path,
            encoding=encoding,
        )

    def __get_pages(self) -> List["BeautifulSoup"]:
        """
        Returns pages with stocks.
        """
        entry_url = self.__site + self.__entry
        return [
            Parser.get_soup(entry_url + hyperlink)
            for hyperlink in get_pagination_hyperlinks(Parser.get_soup(entry_url))
        ]

    def __update(self, page: "BeautifulSoup"):
        """
        Updates `AutoPriorityQueue` instances, also can print `Stock` containers.

        Note:
        -----
        For `self.__low_ratio` queue `-stock.ratio` value
        works as priority for inverting minheap to maxheap.
        """
        for stock in self.__collect_stocks(page):
            if self.__print_stock:
                print(stock)
            if stock.ratio:
                self.__low_ratio.auto_put((-stock.ratio, stock.get_ratio()))
            self.__expensive.auto_put(stock.get_price())
            self.__growthing.auto_put(stock.get_growth())
            self.__profiting.auto_put(stock.get_profit())

    def __collect_stocks(self, page: "BeautifulSoup") -> Iterator["Stock"]:
        """
        Yields `Stock` containers from `page`.
        """
        table = get_stocks_table(page)
        hyperlinks = get_stocks_hyperlinks(table)
        growths = collect_stocks_growths(table)

        for hyperlink, growth in zip(hyperlinks, growths):
            page = Parser.get_soup(self.__site + hyperlink)
            yield get_stock(page, growth)

    @staticmethod
    def __dump_as_json(items: List[Dict], path: str, encoding: str):
        """
        Writes `items` to `path` as JSON in `encoding`.
        """
        with open(file=path, mode="w", encoding=encoding) as as_json:
            dump(items, as_json, indent=4)
