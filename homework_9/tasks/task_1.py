"""
Write a function that merges integer from sorted files and returns an iterator
file1.txt:
1
3
5
file2.txt:
2
4
6

```
list(merge_sorted_files(["file1.txt", "file2.txt"]))
[1, 2, 3, 4, 5, 6]
```
"""
from heapq import merge
from pathlib import Path
from typing import Iterator, List, Optional, Union


# https://medium.com/outco/how-to-merge-k-sorted-arrays-c35d87aa298e
# https://docs.python.org/3.8/library/heapq.html?highlight=merge#heapq.merge
def merge_sorted_files(
    file_list: List[Union[Path, str]], encoding: Optional[str] = "UTF-8"
) -> Iterator[int]:
    """
    Returns generator object witch merge integers from sorted files.

    Example:
    --------
    ```

    >>> file1 = "homework_9/tasks/file1.txt"  # 1, 3, 5
    >>> file2 = Path("homework_9/tasks/file2.txt")  # 2, 4, 6
    >>> list(merge_sorted_files([file1, file2]))
    [1, 2, 3, 4, 5, 6]

    ```
    """

    def get_path(file: Path or str) -> Path:
        return file if isinstance(file, Path) else Path(file)

    return merge(*[_yield_integers(get_path(file), encoding) for file in file_list])


def _yield_integers(file_path: Path, encoding: str) -> Iterator[int]:
    """
    Yields lines as integers from `file_path` with current `encoding`.
    """
    with open(file=file_path, encoding=encoding) as lines:
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.isdigit():
                yield int(stripped_line)
