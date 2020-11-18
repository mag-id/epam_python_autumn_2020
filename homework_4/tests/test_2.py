"""
Unit tests for module `homework_4.tasks.task_2`.
"""
from unittest.mock import Mock, patch

import pytest

from homework_4.tasks.task_2 import URLError, count_dots_on_i

URL = "https://example.com/"
I_NUMBER = 59


@patch("homework_4.tasks.task_2.urlopen")
def test_positive_case_count_dots_on_i(mock_urlopen):
    """
    Passes test if `count_dots_on_i(URL)` result is equal to `I_NUMBER`.
    """
    mock_read = Mock()
    mock_read.read.return_value = "i" * I_NUMBER
    mock_urlopen.return_value = mock_read
    assert count_dots_on_i(URL) == I_NUMBER


@patch("homework_4.tasks.task_2.urlopen")
def test_negative_case_count_dots_on_i(mock_urlopen):
    """
    Passes test if `count_dots_on_i(URL)` raises `ValueError("Unreachable URL")`.
    """
    with pytest.raises(ValueError, match=f"Unreachable {URL}"):
        mock_urlopen.side_effect = URLError("any network error")
        count_dots_on_i(URL)
