"""Conftest for `homework_10.test_stocks.test_derivatives`."""

import sys
from unittest.mock import MagicMock

import pytest

# https://stackoverflow.com/questions/54895002
# https://stackoverflow.com/questions/3108285
sys.path.append("homework_10/stocks")

MOCKED_PACKAGE = "interface.urlopen"


@pytest.fixture
def mock_urlopen(monkeypatch) -> MagicMock:
    """
    Decorator which returns a mock object. Takes `content` as a
    string and mocks `urlopen` at `Parser` interface realization.
    """

    def wrapper(content: str) -> MagicMock:
        """
        Returns a mock object. Takes `content` as a string and
        mocks `urlopen` at `Parser` interface realization.
        """
        package = MOCKED_PACKAGE
        object_ = MagicMock()

        object_.return_value.__enter__.return_value = content
        monkeypatch.setattr(package, object_)

        return object_

    return wrapper
