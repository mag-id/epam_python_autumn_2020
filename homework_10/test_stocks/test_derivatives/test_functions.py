"""Unit tests for module `homework_10.stocks.functions`."""

from typing import Dict, Tuple

import pytest
from bs4 import BeautifulSoup

from homework_10.stocks.functions import (
    collect_stock_code,
    collect_stock_name,
    collect_stock_price,
    collect_stock_profit,
    collect_stock_ratio,
    collect_stocks_growths,
    get_pagination_hyperlinks,
    get_stocks_hyperlinks,
    get_stocks_table,
)

QUOTATION = 2.0
QUOTATION_CONTENT = f"""<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="01.01.2021" name="Foreign Currency Market">
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>{QUOTATION}</Value>
    </Valute>
</ValCurs>
"""

ENTRY = "homework_10/test_stocks/static/entry.html"
PAGINATION_HYPERLINK_STEM = "?p="
ENTRY_DATA = [
    {"hyperlink": "/stocks/mmm-stock", "growth": -3.94},
    {"hyperlink": "/stocks/aos-stock", "growth": 13.89},
    {"hyperlink": "/stocks/abt-stock", "growth": 27.94},
    {"hyperlink": "/stocks/abbv-stock", "growth": 19.13},
    {"hyperlink": "/stocks/acn-stock", "growth": 23.74},
    {"hyperlink": "/stocks/atvi-stock", "growth": 51.81},
    {"hyperlink": "/stocks/adbe-stock", "growth": 45.54},
    {"hyperlink": "/stocks/aap-stock", "growth": 0.24},
    {"hyperlink": "/stocks/aes-stock", "growth": 19.92},
    {"hyperlink": "/stocks/afl-stock", "growth": -18.11},
    {"hyperlink": "/stocks/a-stock", "growth": 41.02},
    {"hyperlink": "/stocks/apd-stock", "growth": 25.01},
    {"hyperlink": "/stocks/akam-stock", "growth": 20.41},
    {"hyperlink": "/stocks/alk-stock", "growth": -25.14},
    {"hyperlink": "/stocks/alb-stock", "growth": 127.91},
    {"hyperlink": "/stocks/are-stock", "growth": 5.94},
    {"hyperlink": "/stocks/alxn-stock", "growth": 47.64},
    {"hyperlink": "/stocks/algn-stock", "growth": 90.17},
    {"hyperlink": "/stocks/alle-stock", "growth": -7.21},
    {"hyperlink": "/stocks/lnt-stock", "growth": -6.51},
    {"hyperlink": "/stocks/all-stock", "growth": -5.24},
    {"hyperlink": "/stocks/googl-stock", "growth": 24.48},
    {"hyperlink": "/stocks/goog-stock", "growth": 24.87},
    {"hyperlink": "/stocks/mo-stock", "growth": -18.20},
    {"hyperlink": "/stocks/amzn-stock", "growth": 69.14},
    {"hyperlink": "/stocks/amd-stock", "growth": 91.71},
    {"hyperlink": "/stocks/aee-stock", "growth": -0.51},
    {"hyperlink": "/stocks/aal-stock", "growth": -43.52},
    {"hyperlink": "/stocks/aep-stock", "growth": -13.07},
    {"hyperlink": "/stocks/axp-stock", "growth": -4.34},
    {"hyperlink": "/stocks/aig-stock", "growth": -26.56},
    {"hyperlink": "/stocks/amt-stock", "growth": -3.43},
    {"hyperlink": "/stocks/awk-stock", "growth": 25.13},
    {"hyperlink": "/stocks/amp-stock", "growth": 11.53},
    {"hyperlink": "/stocks/abc-stock", "growth": 14.69},
    {"hyperlink": "/stocks/ame-stock", "growth": 17.96},
    {"hyperlink": "/stocks/amgn-stock", "growth": -5.22},
    {"hyperlink": "/stocks/aph-stock", "growth": 21.58},
    {"hyperlink": "/stocks/adi-stock", "growth": 27.12},
    {"hyperlink": "/stocks/anss-stock", "growth": 41.34},
    {"hyperlink": "/stocks/antm-stock", "growth": 4.88},
    {"hyperlink": "/stocks/apa-stock", "growth": -36.90},
    {"hyperlink": "/stocks/aapl-stock", "growth": 74.80},
    {"hyperlink": "/stocks/amat-stock", "growth": 49.61},
    {"hyperlink": "/stocks/aptv-stock", "growth": 44.44},
    {"hyperlink": "/stocks/ajg-stock", "growth": 24.74},
    {"hyperlink": "/stocks/spgi-stock", "growth": 17.71},
]

ALLEGION = "homework_10/test_stocks/static/allegion.html"
ALLEGION_DATA = {
    "name": "Allegion PLC",
    "code": "ALLE",
    "price": round(119.98 * QUOTATION, 2),
    "P/E": False,
    "potential profit": 79.94,
    "growth": -7.21,
}

AMAZON = "homework_10/test_stocks/static/amazon.html"
AMAZON_DATA = {
    "name": "Amazon",
    "code": "AMZN",
    "price": round(3181.10 * QUOTATION, 2),
    "P/E": 81.55,
    "potential profit": 118.19,
    "growth": 69.14,
}


def load_page(path: str) -> BeautifulSoup:
    """
    Returns page from HTML file at the `path`.
    """
    with open(file=path, mode="r", encoding="utf-8") as text:
        return BeautifulSoup(text.read())


# pylint: disable=redefined-outer-name


@pytest.fixture
def entry_page() -> BeautifulSoup:
    """
    Returns `ENTRY` page.
    """
    return load_page(ENTRY)


@pytest.fixture(params=[(ALLEGION_DATA, ALLEGION), (AMAZON_DATA, AMAZON)])
def stock_data_and_page(request) -> Tuple[Dict[str, float], BeautifulSoup]:
    """
    Returns pairs of stock data and stock page:
    + `ALLEGION_DATA` and `ALLEGION` page.
    + `AMAZON_DATA` and `AMAZON` page.
    """
    data, path = request.param
    return data, load_page(path)


def test_get_pagination_hyperlinks(entry_page):
    """
    Passes test if `get_pagination_hyperlinks`
    returns valid hyperlinks from `entry_page`.
    """
    ten_hyperlinks = [PAGINATION_HYPERLINK_STEM + str(num) for num in range(1, 11)]
    assert get_pagination_hyperlinks(entry_page) == ten_hyperlinks


def test_get_stocks_table(entry_page):
    """
    Passes test if `get_stocks_table` returns `BeautifulSoup`
    object with valid number of the entries from `entry_page`.
    """
    table = get_stocks_table(entry_page)
    assert len(ENTRY_DATA) == len(table)


def test_get_stocks_hyperlinks(entry_page):
    """
    Passes test if `get_stocks_hyperlinks`
    returns valid hyperlinks from `entry_page`.
    """
    table = entry_page.find("table", class_="table table-small").find_all("tr")[1:]
    assert [row["hyperlink"] for row in ENTRY_DATA] == get_stocks_hyperlinks(table)


def test_collect_stocks_growths(entry_page):
    """
    Passes test if `get_stocks_hyperlinks` returns
    valid `"growth"` values for stocks from `entry_page`.
    """
    table = entry_page.find("table", class_="table table-small").find_all("tr")[1:]
    assert [row["growth"] for row in ENTRY_DATA] == collect_stocks_growths(table)


def test_collect_stock_name(stock_data_and_page):
    """
    Passes test if the result of the `collect_stock_name`
    for a stock page equals to the stock `"name"`.
    """
    expected_result, page = stock_data_and_page
    assert expected_result["name"] == collect_stock_name(page)


def test_collect_stock_code(stock_data_and_page):
    """
    Passes test if the result of the `collect_stock_code`
    for a stock page equals to the stock `"code"`.
    """
    expected_result, page = stock_data_and_page
    assert expected_result["code"] == collect_stock_code(page)


def test_collect_stock_price(mock_urlopen, stock_data_and_page):
    """
    Passes test if the result of the `collect_stock_price`
    for a stock page equals to the stock `"price"`.
    """
    _ = mock_urlopen(QUOTATION_CONTENT)
    expected_result, page = stock_data_and_page
    assert expected_result["price"] == round(collect_stock_price(page), 2)


def test_collect_stock_ratio(stock_data_and_page):
    """
    Passes test if the result of the `collect_stock_ratio`
    for a stock page equals to the stock `"P/E"`.
    """
    expected_result, page = stock_data_and_page
    assert expected_result["P/E"] == collect_stock_ratio(page)


def test_collect_stock_profit(stock_data_and_page):
    """
    Passes test if the result of the `collect_stock_profit`
    for a stock page equals to the stock `"potential profit"`.
    """
    expected_result, page = stock_data_and_page
    assert expected_result["potential profit"] == round(collect_stock_profit(page), 2)
