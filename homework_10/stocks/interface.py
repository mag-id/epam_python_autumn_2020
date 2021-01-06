"""Interface."""

from abc import ABC
from typing import Any, Callable, Dict, List
from urllib.request import urlopen

from bs4 import BeautifulSoup

__all__ = ["Parser"]


class Parser(ABC):
    """
    Implements `Parser` interface:

    + `execute` - `Parser` start method, not implemented.

    + `get_soup` - returns `BeautifulSoup` from `url` string of
    the HTML page. By default `parser` is `"lxml"`.

    + `get_data` - returns `Any` data from `soup` which found
    by `finding_function` and parsed by `parsing_function`.
    """

    @staticmethod
    def execute() -> List[Dict]:
        """
        `Parser` start method, not implemented.
        """
        raise NotImplementedError

    @staticmethod
    def get_soup(url: str, parser="lxml") -> BeautifulSoup:
        """
        Returns `BeautifulSoup` from `url` string of the HTML page.
        By default `parser` is `"lxml"`.
        """
        with urlopen(url) as html:
            return BeautifulSoup(html, parser)

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
