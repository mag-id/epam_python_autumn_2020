"""
Unit tests for module `homework_4.tasks.task_2`.
"""
from unittest.mock import MagicMock
from urllib.request import URLError

import pytest

from homework_4.tasks.task_2 import count_dots_on_i

URL = "https://mocked_example.com/"
CONTENT = b"<html>\n<head>iii</head>\n<body>\niii\n</body>\n</html>"
I_NUMBER = 6


def test_positive_case_count_dots_on_i(monkeypatch):
    """
    Passes test if `count_dots_on_i(URL)` result is equal to `I_NUMBER` according to `CONTENT`.
    """
    mocked_urlopen = MagicMock()
    # https://stackoverflow.com/questions/38199008/python-returns-magicmock-object-instead-of-return-value
    mocked_urlopen().read.return_value = CONTENT
    monkeypatch.setattr("homework_4.tasks.task_2.urlopen", mocked_urlopen)
    assert count_dots_on_i(URL) == I_NUMBER


def test_negative_case_count_dots_on_i(monkeypatch):
    """
    Passes test if `count_dots_on_i(URL)` raises `ValueError("Unreachable URL")`.
    """
    monkeypatch.setattr(
        "homework_4.tasks.task_2.urlopen",
        MagicMock(side_effect=URLError(404)),
    )
    with pytest.raises(ValueError, match=f"Unreachable {URL}"):
        count_dots_on_i(URL)
