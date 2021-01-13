"""Unit tests for module `homework_10.stocks.usd_to_rub`."""

from homework_10.stocks.usd_to_rub import get_usd_rub_quotation, usd_to_rub

CONTENT = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="01.01.2021" name="Foreign Currency Market">
    <Valute ID="R01200">
        <NumCode>344</NumCode>
        <CharCode>HKD</CharCode>
        <Nominal>10</Nominal>
        <Name>Гонконгских долларов</Name>
        <Value>95,3013</Value>
    </Valute>
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>73,8757</Value>
    </Valute>
</ValCurs>
"""


# pylint: disable=redefined-outer-name


def test_get_usd_rub_quotation(mock_urlopen):
    """
    Passes test  if `get_usd_rub_quotation` returns valid value for `CONTENT`.
    """
    _ = mock_urlopen(CONTENT)
    assert get_usd_rub_quotation() == 73.8757


def test_usd_to_rub(mock_urlopen):
    """
    Passes test if `usd_to_rub` makes only one request.
    """
    mock_object = mock_urlopen(CONTENT)

    @usd_to_rub
    def get_value(value: int) -> float:
        return float(value)

    get_value(1)
    get_value(2)
    get_value(3)

    assert mock_object.call_count == 1
