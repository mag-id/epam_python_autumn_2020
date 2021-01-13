"""Realization of the parsing functions via `Parser` from `stocks.interface`."""

from re import search
from typing import List

from bs4 import BeautifulSoup
from container import Stock
from interface import Parser
from usd_to_rub import usd_to_rub

__all__ = [
    "get_stock",
    "get_pagination_hyperlinks",
    "get_stocks_table",
    "get_stocks_hyperlinks",
    "collect_stocks_growths",
]


def get_stock(stock: BeautifulSoup, growth: float) -> Stock:
    """
    Returns filled `Stock` instance. `price` and `profit` round to the hundredths.
    """
    return Stock(
        name=collect_stock_name(stock),
        code=collect_stock_code(stock),
        price=round(collect_stock_price(stock), 2),
        ratio=collect_stock_ratio(stock),
        growth=growth,
        profit=round(collect_stock_profit(stock), 2),
    )


def get_pagination_hyperlinks(page: BeautifulSoup) -> List[str]:
    """
    Returns pagination hyperlinks from `page`.
    """
    return Parser.get_data(
        soup=page,
        filter_=lambda page: page.find("div", class_="finando_paging"),
        prepare=lambda page: [entry["href"] for entry in page.find_all("a")],
    )


def get_stocks_table(page: BeautifulSoup) -> BeautifulSoup:
    """
    Returns content of the table (without head) from `page`.
    """
    return Parser.get_data(
        soup=page,
        filter_=lambda page: page.find("table", class_="table table-small"),
        prepare=lambda page: page.find_all("tr")[1:],
    )


def get_stocks_hyperlinks(table: BeautifulSoup) -> List[str]:
    """
    Returns hyperlinks of the stocks from the `table`.
    """
    return Parser.get_data(
        soup=table,
        filter_=lambda table: [row.find("a") for row in table],
        prepare=lambda table: [row["href"] for row in table],
    )


def collect_stocks_growths(table: BeautifulSoup) -> List[float]:
    """
    Returns year growth of the stock in percentages from the `table`.
    """
    return Parser.get_data(
        soup=table,
        filter_=lambda table: [row.find_all("span")[-1] for row in table],
        prepare=lambda table: [float(row.string.rstrip("%")) for row in table],
    )


def collect_stock_name(stock: BeautifulSoup) -> str:
    """
    Returns name of the `stock`.
    """
    return Parser.get_data(
        soup=stock,
        filter_=lambda stock: stock.find("span", class_="price-section__label"),
        prepare=lambda stock: stock.string.strip(),
    )


def collect_stock_code(stock: BeautifulSoup) -> str:
    """
    Returns code of the `stock`.
    """
    return Parser.get_data(
        soup=stock,
        filter_=lambda stock: stock.find("span", class_="price-section__category"),
        prepare=lambda stock: stock.text.split(",")[-1].strip(),
    )


@usd_to_rub
def collect_stock_price(stock: BeautifulSoup) -> float:
    """
    Returns price of the `stock` in USD.
    """
    return Parser.get_data(
        soup=stock,
        filter_=lambda stock: stock.find("span", class_="price-section__current-value"),
        prepare=lambda stock: float(stock.text.replace(",", "")),
    )


def collect_stock_ratio(stock: BeautifulSoup) -> float or False:
    """
    Returns P/E ratio of the `stock`. If
    not found, `False` will be returned.
    """
    try:
        return Parser.get_data(
            soup=stock,
            filter_=lambda stock: stock.find("div", string="P/E Ratio").find_parent(
                "div", class_="snapshot__data-item"
            ),
            prepare=lambda stock: float(stock.text.split()[0].replace(",", "")),
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
        filter_=lambda soup: stock.find("div", class_="snapshot").find("script").string,
        prepare=calculate_profit,
    )
