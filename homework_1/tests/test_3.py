"""
Unit tests for module `homework_1.tasks.task_3`.
"""

from tempfile import NamedTemporaryFile
from typing import Tuple

import pytest

from homework_1.tasks.task_3 import find_maximum_and_minimum


@pytest.mark.parametrize(
    ["file_content", "expected_result"],
    [
        pytest.param(
            "0\n",
            (0, 0),
            id="File content is '0\n', result is (0, 0).",
        ),
        pytest.param(
            "1\n2\n3\n4\n5\n",
            (1, 5),
            id="File content is '1\n2\n3\n4\n5\n', result is (1, 5).",
        ),
        pytest.param(
            "\n".join(str(num) for num in range(0, 667000)),
            (0, 666999),
            id="File content is integers from 0 to 666999 delimited by '\n'.",
        ),
    ],
)
def test_find_maximum_and_minimum(file_content: str, expected_result: Tuple[int, int]):
    """
    Mocks file using `NamedTemporaryFile` instance with writed
    `file_content` inside, where `file_name` == `file.name`.

    Passes test if `find_maximum_and_minimum`(`file.name`)
    is equal to `expected_result`.
    """
    with NamedTemporaryFile(mode="wt") as file:
        file.write(file_content)
        file.seek(0)
        actual_result = find_maximum_and_minimum(file.name)

    assert actual_result == expected_result
