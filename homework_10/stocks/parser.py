"""Realization of the `StocksParser` by `Parser` from `stocks.interface`."""

from concurrent.futures import ThreadPoolExecutor
from re import search
from typing import Dict, Iterator, List

from bs4 import BeautifulSoup
from interface import Parser
from usd_to_rub import usd_to_rub

__all__ = ["SITE", "ENTRY", "StocksParser"]

SITE = "https://markets.businessinsider.com"
ENTRY = "/index/components/s&p_500"

UNEQUAL = "Number of the stocks hyperlinks and growths are not equal."


# pylint: disable=too-few-public-methods
class StocksParser:
    """
    `Parser` realization for
    `https://markets.businessinsider.com/index/components/s&p_500`.

    Collect for each stock next data from [S&P 500
    ](https://en.wikipedia.org/wiki/S%26P_500_Index) list:

    + "name" - Stock name, `str`.

    + "code" - Stock code, `str`.

    + "price" - Stock price in RUB according to USD-RUB [daily quotation
    ](http://www.cbr.ru/scripts/XML_daily.asp)
    according to [The Central Bank of the Russian Federation
    ](http://www.cbr.ru/development/sxml/), `float` RUB.

    + "P/E" - [Price-earnings (P/E) ratio
    ](https://en.wikipedia.org/wiki/Price–earnings_ratio)
    of a stock, `float`. If not found - returns `False`.

    + "potential profit" - the difference between [Week High 52 and Week Low 52
    ](https://www.investopedia.com/terms/1/52weekhighlow.asp), `float` percentages.

    + "growth" - Stock year growth, `float` percentages.

    Note:
    -----
    `price` and `potential profit` round to the hundredths.

    Formula:
    --------
    `potential profit` = (100% * 52 Week High) / 52 Week Low - 100%.
    """

    @staticmethod
    def execute() -> List[Dict[str, str or float]]:
        """
        `StocksParser` start method.
        """

        def assemble(page: BeautifulSoup):
            assembled.extend(list(yield_stocks(page)))

        assembled = []
        pages = list(yield_pages(SITE + ENTRY))

        with ThreadPoolExecutor(max_workers=len(pages)) as executor:
            executor.map(assemble, pages)

        return assembled


def yield_pages(url: str) -> Iterator[BeautifulSoup]:
    """
    Yields pages with stocks from `url`.
    """
    page = Parser.get_soup(url)
    for hyperlink in _get_pagination_hyperlinks(page):
        yield Parser.get_soup(url + hyperlink)


def _get_pagination_hyperlinks(page: BeautifulSoup) -> List[str]:
    """
    Returns pagination hyperlinks from `page`.
    """
    return Parser.get_data(
        soup=page,
        finding_function=lambda page: page.find("div", class_="finando_paging"),
        parsing_function=lambda page: [entry["href"] for entry in page.find_all("a")],
    )


def yield_stocks(page: BeautifulSoup) -> Iterator[Dict[str, str or float]]:
    """
    Yields stocks data from `page`.
    """
    table = _get_stocks_table(page)
    hyperlinks = _get_stocks_hyperlinks(table)
    growths = collect_stocks_growths(table)

    if len(hyperlinks) != len(growths):
        raise IndexError(UNEQUAL)

    for hyperlink, growth in zip(hyperlinks, growths):
        stock = Parser.get_soup(SITE + hyperlink)
        yield collect_stock(stock, growth)


def _get_stocks_table(page: BeautifulSoup) -> BeautifulSoup:
    """
    Returns content of the table (without head) from `page`.
    """
    return Parser.get_data(
        soup=page,
        finding_function=lambda page: page.find("table", class_="table table-small"),
        parsing_function=lambda page: page.find_all("tr")[1:],
    )


def _get_stocks_hyperlinks(table: BeautifulSoup) -> List[str]:
    """
    Returns hyperlinks of the stocks from the `table`.
    """
    return Parser.get_data(
        soup=table,
        finding_function=lambda table: [row.find("a") for row in table],
        parsing_function=lambda table: [row["href"] for row in table],
    )


def collect_stocks_growths(table: BeautifulSoup) -> List[float]:
    """
    Returns year growth of the stock in percentages from the `table`.
    """
    return Parser.get_data(
        soup=table,
        finding_function=lambda table: [row.find_all("span")[-1] for row in table],
        parsing_function=lambda table: [float(row.string.rstrip("%")) for row in table],
    )


def collect_stock(stock: BeautifulSoup, growth: float) -> Dict:
    """
    Collects `stock` and it's `growth` data in one dictionary.

    Note: `price` and `potential profit` round to the hundredths.
    """
    return {
        "name": collect_stock_name(stock),
        "code": collect_stock_code(stock),
        "price": round(collect_stock_price(stock), 2),
        "P/E": collect_stock_ratio(stock),
        "potential profit": round(collect_stock_profit(stock), 2),
        "growth": growth,
    }


def collect_stock_name(stock: BeautifulSoup) -> str:
    """
    Returns name of the `stock`.
    """
    return Parser.get_data(
        soup=stock,
        finding_function=lambda stock: stock.find(
            "span", class_="price-section__label"
        ),
        parsing_function=lambda stock: stock.string.strip(),
    )


def collect_stock_code(stock: BeautifulSoup) -> str:
    """
    Returns code of the `stock`.
    """
    return Parser.get_data(
        soup=stock,
        finding_function=lambda stock: stock.find(
            "span", class_="price-section__category"
        ),
        parsing_function=lambda stock: stock.text.split(",")[-1].strip(),
    )


@usd_to_rub
def collect_stock_price(stock: BeautifulSoup) -> float:
    """
    Returns price of the `stock` in USD.
    """
    return Parser.get_data(
        soup=stock,
        finding_function=lambda stock: stock.find(
            "span", class_="price-section__current-value"
        ),
        parsing_function=lambda stock: float(stock.text.replace(",", "")),
    )


def collect_stock_ratio(stock: BeautifulSoup) -> float or False:
    """
    Returns P/E ratio of the `stock`. If
    not found, `False` will be returned.
    """
    try:
        return Parser.get_data(
            soup=stock,
            finding_function=lambda stock: stock.find(
                "div", string="P/E Ratio"
            ).find_parent("div", class_="snapshot__data-item"),
            parsing_function=lambda stock: float(
                stock.text.split()[0].replace(",", "")
            ),
        )
    except AttributeError:
        return False


def collect_stock_profit(stock: BeautifulSoup) -> float:
    """
    Returns potential profit of the `stock` in percentages.

    Formula: `(100% * 52 Week High) / 52 Week Low - 100%`.
    """

    def parse(expression: str, script: str) -> float:
        return float(search(expression, script).group(1))

    def calculate_profit(script: str) -> float:
        high = parse(r"high52weeks:\s*(\d*\.?\d*)", script)
        low = parse(r"low52weeks:\s*(\d*\.?\d*)", script)
        return (100 * high) / low - 100

    return Parser.get_data(
        soup=stock,
        finding_function=lambda soup: stock.find("div", class_="snapshot")
        .find("script")
        .string,
        parsing_function=calculate_profit,
    )
