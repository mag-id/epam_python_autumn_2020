"""Unit tests for module `homework_10.stocks.interface`."""

from typing import Any, Callable
from unittest.mock import MagicMock

import pytest
from bs4 import BeautifulSoup

from homework_10.stocks.interface import Parser

MOCKED_PACKAGE = "homework_10.stocks.interface.urlopen"
URL = "https://test_page.com/"
CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<title>Test Page</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>

<div class="header">
	<h1>Header</h1>
	<p>A <b>test</b> page.</p>
</div>

<div class="navbar">
	<h2>Bar</h2>
	<a href="#" class="active">Home</a>
	<a href="#">Link 1</a>
	<a href="#">Link 2</a>
	<a href="#" class="right">Link 3</a>
</div>

<div class="row">
	<h2>Content</h2>
	<div class="side">  
		<p>Text in the side content.</p>
	</div>
	<div class="main">
		<p>Text in the main content.</p>
	</div>
</div>

<div class="footer">
	<h2>Footer</h2>
	<p>Text in the footer.</p>
</div>
</body>
</html>
"""


def test_execute():
    """
    Passes test if `Parser.execute` raises `NotImplementedError`.
    """
    with pytest.raises(NotImplementedError):
        Parser.execute()


# pylint: disable=redefined-outer-name
# https://stackoverflow.com/questions/28850070
@pytest.mark.parametrize(
    ["parser"],
    [
        pytest.param("lxml", id="URL CONTENT by 'lxml' parser."),
        pytest.param("lxml-xml", id="URL CONTENT by 'lxml-xml' parser."),
        pytest.param("html.parser", id="URL CONTETN by 'html.parsers' parser."),
    ],
)
def test_get_soup(monkeypatch, parser: str):
    """
    Passes test if the `Parser.get_soup` data not corrupted by different parsers.
    """
    package = MOCKED_PACKAGE
    object_ = MagicMock()
    object_.return_value.__enter__.return_value = CONTENT
    monkeypatch.setattr(package, object_)

    result = Parser.get_soup(url=URL, parser=parser)
    expected_result = BeautifulSoup(CONTENT)
    assert result.string == expected_result.string


@pytest.mark.parametrize(
    ["filter_", "prepare", "expected_result"],
    [
        pytest.param(
            lambda soup: soup.find("script"), bool, False, id="No <script> in CONTENT."
        ),
        pytest.param(
            lambda soup: soup.find_all("div"),
            len,
            6,
            id="Number of <dev ...> in CONTENT is 6.",
        ),
        pytest.param(
            lambda soup: soup.find_all("title"),
            lambda soup: (len(soup), soup[0].text),
            (1, "Test Page"),
            id="Number of <title> in CONTENT is 1 and its text is 'Test Page'.",
        ),
    ],
)
def test_get_data(filter_: Callable, prepare: Callable, expected_result: Any):
    """
    Passes test if `Parser.get_data` works correctly along
    with `BeautifulSoup(CONTENT, parser="html.parser")`,
    `filter_` and `prepare` functions.
    """
    result = Parser.get_data(
        soup=BeautifulSoup(CONTENT, parser="html.parser"),
        filter_=filter_,
        prepare=prepare,
    )
    assert result == expected_result
