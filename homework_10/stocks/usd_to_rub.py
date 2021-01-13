"""Tools for conversion USD to RUB via `Parser` from `stocks.interface`."""

from typing import Callable

from interface import Parser

__all__ = ["get_usd_rub_quotation", "usd_to_rub"]

SITE = "http://www.cbr.ru/scripts/XML_daily.asp"
USD_ID = "R01235"


def usd_to_rub(function: Callable) -> float:
    """
    The decorator which converts USD to RUB.

    Takes USD-RUB [daily quotation
    ](http://www.cbr.ru/scripts/XML_daily.asp)
    according to [The Central Bank of the Russian Federation
    ](http://www.cbr.ru/development/sxml/).

    See `get_usd_rub_quotation`.
    """

    cached = []

    def wrapper(value: float or int) -> float:
        if not cached:
            cached.append(get_usd_rub_quotation())
        return cached[0] * function(value)

    return wrapper


def get_usd_rub_quotation() -> float:
    """
    Returns USD-RUB [daily quotation
    ](http://www.cbr.ru/scripts/XML_daily.asp)
    according to [The Central Bank of the Russian Federation
    ](http://www.cbr.ru/development/sxml/).
    """
    return Parser.get_data(
        soup=Parser.get_soup(SITE, parser="lxml-xml"),
        filter_=lambda xml: xml.find("Valute", ID=USD_ID).find("Value"),
        prepare=lambda value: float(value.string.replace(",", ".")),
    )
