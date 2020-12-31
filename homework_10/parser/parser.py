"""
In progress
"""

from abc import ABC
from re import search
from typing import Any, Callable, List
from urllib.request import urlopen

# import aiohttp
from bs4 import BeautifulSoup

# pylint: disable=too-few-public-methods


class Page(ABC):
    """
    Implements `Page` interface:

    + `get_soup` - returns `BeautifulSoup` from `url` string of
    the HTML page.

    + `get_data` - returns `Any` data from `soup` which found
    by `finding_function` and parsed by `parsing_function`.
    """

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        """
        Returns `BeautifulSoup` from `url` string of the HTML page.
        """
        with urlopen(url) as html:
            return BeautifulSoup(html, "html.parser")

    @staticmethod
    def get_data(
        soup: BeautifulSoup,
        finding_function: Callable,
        parsing_function: Callable,
    ) -> Any:
        """
        Returns `Any` data from `soup` which found by
        `finding_function` and parsed by `parsing_function`.
        """
        return parsing_function(finding_function(soup))


class PaginationPage:
    """
    Takes `url` of the entry (start) page.

    Initializes instance with `hyperlinks`
    attribute with hyperlinks of the pages.
    """

    def __init__(self, url: str):
        self.hyperlinks = self.__get_hyperlinks(url)

    @staticmethod
    def __get_hyperlinks(url: str) -> List[str]:
        """
        Returns hyperlinks of the pages.
        """
        return Page.get_data(
            soup=Page.get_soup(url),
            finding_function=lambda soup: soup.find("div", class_="finando_paging"),
            parsing_function=lambda soup: [row["href"] for row in soup.find_all("a")],
        )


class StockTablePage:
    """
    Takes `url` of the page according `PaginationPage`.

    Initializes instance with next attributes:
    + `hyperlinks` - hyperlinks of the stock pages.
    + `year_growths` - year growth of the stock in percents.
    """

    def __init__(self, url: str):
        self.__table = self.__get_table(url)

        self.hyperlinks = self.__get_hyperlinks()
        self.year_growths = self.__get_year_growths()

    @staticmethod
    def __get_table(url) -> BeautifulSoup:
        """
        Returns content of `table` tag with `table table-small` class
        without table head from HTML page at `url` as `BeautifulSoup` instance.
        """
        return Page.get_data(
            soup=Page.get_soup(url),
            finding_function=lambda soup: soup.find(
                "table", class_="table table-small"
            ),
            parsing_function=lambda soup: soup.find_all("tr")[1:],
        )

    def __get_hyperlinks(self) -> List[str]:
        """
        Returns hyperlinks of the stocks.
        """
        return Page.get_data(
            soup=self.__table,
            finding_function=lambda soup: [entry.find("a") for entry in soup],
            parsing_function=lambda soup: [entry["href"] for entry in soup],
        )

    def __get_year_growths(self) -> List[float]:
        """
        Returns year growth of the stock in percents.
        """
        return Page.get_data(
            soup=self.__table,
            finding_function=lambda soup: [
                entry.find_all("span")[-1] for entry in soup
            ],
            parsing_function=lambda soup: [
                float(entry.string.rstrip("%")) for entry in soup
            ],
        )


class StockPage:
    """
    Attributes:
    + `name`
    + `code`
    + `price`
    + `ratio`
    + `potential_profit`
    """

    def __init__(self, url: str):
        self.__soup = Page.get_soup(url)

        self.name = self.__get_name()
        self.code = self.__get_code()
        self.price = self.__get_price()
        self.ratio = self.__get_ratio()
        self.potential_profit = self.__get_potential_profit()

    def __get_name(self) -> str:
        """
        Returns name of the stock.
        """
        return Page.get_data(
            soup=self.__soup,
            finding_function=lambda soup: soup.find(
                "span", class_="price-section__label"
            ),
            parsing_function=lambda soup: soup.string.strip(),
        )

    def __get_code(self) -> str:
        """
        Returns code of the stock.
        """
        return Page.get_data(
            soup=self.__soup,
            finding_function=lambda soup: soup.find(
                "span", class_="price-section__category"
            ),
            parsing_function=lambda soup: soup.text.split(",")[-1].strip(),
        )

    def __get_price(self) -> float:
        """
        Returns price of the stock.
        """
        return Page.get_data(
            soup=self.__soup,
            finding_function=lambda soup: soup.find(
                "span", class_="price-section__current-value"
            ),
            parsing_function=lambda soup: float(soup.text.replace(",", "")),
        )

    def __get_ratio(self) -> float:
        """
        Returns P/E ratio of the stock.
        If it can not be founded, `0.0`
        will be retuned.
        """
        try:
            return Page.get_data(
                soup=self.__soup,
                finding_function=lambda soup: soup.find(
                    "div", string="P/E Ratio"
                ).find_parent("div", class_="snapshot__data-item"),
                parsing_function=lambda soup: float(soup.text.split()[0]),
            )
        except AttributeError:
            return 0.0

    def __get_potential_profit(self) -> float:
        """
        Retruns potencial profit of the stock
        in percents rounded to hundreds.
        """

        def parse(expression: str, script: str) -> float:
            return float(search(expression, script).group(1))

        def calculate_profit(script: str) -> float:
            high = parse(r"high52weeks:\s*(\d*\.?\d*)", script)
            low = parse(r"low52weeks:\s*(\d*\.?\d*)", script)
            return round(((high - low) * 100 / low), 2)

        return Page.get_data(
            soup=self.__soup,
            finding_function=lambda soup: soup.find("div", class_="snapshot")
            .find("script")
            .string,
            parsing_function=calculate_profit,
        )


def main():
    """
    In progress
    """
    stem = "https://markets.businessinsider.com/"
    entry_hyperlink = "index/components/s&p_500"

    for stocks_list in PaginationPage(stem + entry_hyperlink).hyperlinks:

        stocks_list = StockTablePage(stem + entry_hyperlink + stocks_list)
        pairs = zip(stocks_list.hyperlinks, stocks_list.year_growths)

        for hyperlink, year_growths in pairs:
            current = StockPage(stem + hyperlink)

            print(
                current.name,
                current.code,
                current.price,
                current.ratio,
                year_growths,
                current.potential_profit,
            )


if __name__ == "__main__":
    main()
