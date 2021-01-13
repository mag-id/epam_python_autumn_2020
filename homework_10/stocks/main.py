"""`StocksParser` entry point."""

from pathlib import Path

from stocks_parser import StocksParser


def main(  # pylint: disable=too-many-arguments
    directory: str,
    top_low_ratio_stocks: str = "top_low_ratio_stocks.json",
    top_expensive_stocks: str = "top_expensive_stocks.json",
    top_growthing_stocks: str = "top_growthing_stocks.json",
    top_profiting_stocks: str = "top_profiting_stocks.json",
    queue_cache: int = 10,
    max_workers: int = None,
    print_stock: bool = False,
):
    """
    Execute `StocksParser` and saves to the `directory`:

    + `top_low_ratio_stocks` - The lowest P/E ratio stocks.
    Name is `"top_low_ratio_stocks.json"` by default.

    + `top_expensive_stocks` - The most expensive stocks with prices in RUB.
    Name is `"top_expensive_stocks.json"` by default.

    + `top_growthing_stocks` - The most growing stocks at last year in percentage.
    Name is `"top_expensive_stocks.json"` by default.

    + `top_profiting_stocks` - The most potentially profiting stocks.
    Name is `"top_expensive_stocks.json"` by default.

    in JSON format
    ```
    [{"ratio" | "price" | "growth" | "profit": float, "name": str, "code": str}]
    ```

    Default key-value arguments:
    ----------------------------
    + `queue_cache` - Number of stocks to write. `10` by default.
    + `max_workers` - Max number of threads for pages parsing.
    `None` by default i.e. number of pagination pages.
    + `print_stock` - Prints whole raw stock info in StdOut.
    `False` by default.
    """
    directory = Path(directory)
    directory.mkdir(exist_ok=True)

    parsed_stocks = StocksParser(
        queue_cache=queue_cache,
        max_workers=max_workers,
        print_stock=print_stock,
    )
    parsed_stocks.execute()

    parsed_stocks.dump_low_ratio(directory / top_low_ratio_stocks)
    parsed_stocks.dump_expensive(directory / top_expensive_stocks)
    parsed_stocks.dump_growthing(directory / top_growthing_stocks)
    parsed_stocks.dump_profiting(directory / top_profiting_stocks)


if __name__ == "__main__":
    main("homework_10/data/")
