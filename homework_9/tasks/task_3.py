"""
Write a function that takes directory path, a file extension and an optional tokenizer.
It will count lines in all files with that extension if there are no tokenizer.
If a the tokenizer is not none, it will count tokens.

For dir with two files from hw1.py:
```

>>> test_dir = Path("homework_9/tasks")
>>> universal_file_counter(test_dir, "txt")
6
>>> universal_file_counter(test_dir, "txt", str.split)
6

```
"""
from pathlib import Path
from typing import Callable, Iterator, Optional

DOT = "."
ALL = "*"


def universal_file_counter(
    dir_path: Path,
    file_extension: str,
    tokenizer: Optional[Callable] = None,
    encoding: Optional[str] = "UTF-8",
) -> int:
    """
    Returns number of tokens for all files at `dir_path` with current `file_extension`.
    If `tokenizer` is not specified, the number of lines returns. `encoding` is "UTF-8"
    by default.
    """
    number_of_tokens = 0
    for file in _get_files(dir_path, file_extension):
        for line in _get_lines(file, encoding):

            if tokenizer:
                number_of_tokens += len(tokenizer(line))
            else:
                number_of_tokens += 1

    return number_of_tokens


def _get_files(dir_path: Path, file_extension: str) -> Iterator[Path]:
    """
    Returns `Generator[Path]` from `dir_path` with current `file_extension`.
    """
    if not file_extension.startswith(DOT):
        file_extension = DOT + file_extension
    return dir_path.glob(ALL + file_extension)


def _get_lines(file_path: Path, encoding: str) -> Iterator[str]:
    """
    Yields lines from `file_path` with current `encoding`.
    """
    with open(file=file_path, encoding=encoding) as lines:
        for line in lines:
            yield line
