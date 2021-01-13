"""Container for stocks data."""

from dataclasses import dataclass, field

__all__ = ["Stock"]


@dataclass(frozen=True, order=True)
class StockPrice:
    """
    + `name` - Stock name, `str`.

    + `code` - Stock code, `str`.

    + `price` - Stock price in RUB according to USD-RUB [daily quotation
    ](http://www.cbr.ru/scripts/XML_daily.asp)
    according to [The Central Bank of the Russian Federation
    ](http://www.cbr.ru/development/sxml/), `float` RUB.
    """

    price: float
    name: str = field(compare=False)
    code: str = field(compare=False)


@dataclass(frozen=True, order=True)
class StockRatio:
    """
    + `name` - Stock name, `str`.

    + `code` - Stock code, `str`.

    + `ratio` - [Price-earnings (P/E) ratio
    ](https://en.wikipedia.org/wiki/Price–earnings_ratio)
    of a stock, `float`. If not found - returns `False`.
    """

    ratio: float
    name: str = field(compare=False)
    code: str = field(compare=False)


@dataclass(frozen=True, order=True)
class StockGrowth:
    """
    + `name` - Stock name, `str`.

    + `code` - Stock code, `str`.

    + `growth` - Stock year growth, `float` percentages.
    """

    growth: float
    name: str = field(compare=False)
    code: str = field(compare=False)


@dataclass(frozen=True, order=True)
class StockProfit:
    """
    + `name` - Stock name, `str`.

    + `code` - Stock code, `str`.

    + `profit` - potencial profit, the difference between [Week High 52 and Week Low 52
    ](https://www.investopedia.com/terms/1/52weekhighlow.asp), `float` percentages.

    Formula:
    --------
    potential profit = (100% * 52 Week High) / 52 Week Low - 100%.
    """

    profit: float
    name: str = field(compare=False)
    code: str = field(compare=False)


@dataclass(eq=False, frozen=True)
class Stock:
    """
    + `name` - Stock name, `str`.

    + `code` - Stock code, `str`.

    + `price` - Stock price in RUB according to USD-RUB [daily quotation
    ](http://www.cbr.ru/scripts/XML_daily.asp)
    according to [The Central Bank of the Russian Federation
    ](http://www.cbr.ru/development/sxml/), `float` RUB.

    + `ratio` - [Price-earnings (P/E) ratio
    ](https://en.wikipedia.org/wiki/Price–earnings_ratio)
    of a stock, `float`. If not found - returns `False`.

    + `growth` - Stock year growth, `float` percentages.

    + `profit` - potencial profit, the difference between [Week High 52 and Week Low 52
    ](https://www.investopedia.com/terms/1/52weekhighlow.asp), `float` percentages.

    Formula:
    --------
    potential profit = (100% * 52 Week High) / 52 Week Low - 100%.
    """

    name: str = field(compare=False)
    code: str = field(compare=False)
    price: float = field(compare=False)
    ratio: float = field(compare=False)
    growth: float = field(compare=False)
    profit: float = field(compare=False)

    def get_price(self) -> StockPrice:
        """
        Returns `StockPrice`.
        """
        return StockPrice(self.price, self.name, self.code)

    def get_ratio(self) -> StockRatio:
        """
        Returns `StockRatio`.
        """
        return StockRatio(self.ratio, self.name, self.code)

    def get_growth(self) -> StockGrowth:
        """
        Returns `StockGrowth`.
        """
        return StockGrowth(self.growth, self.name, self.code)

    def get_profit(self) -> StockProfit:
        """
        Returns `StockProfit`.
        """
        return StockProfit(self.profit, self.name, self.code)
