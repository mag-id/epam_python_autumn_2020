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
            id="'0\n', result is (0, 0).",
        ),
        pytest.param(
            "1\n2\n3\n4\n5\n",
            (1, 5),
            id="'1\n2\n3\n4\n5\n', result is (1, 5).",
        ),
        pytest.param(
            "1\n-2\n3\n-4\n5\n-6\n7\n-8\n9\n-10\n11\n-12\n",
            (-12, 11),
            id="'1\n-2\n3\n-4\n5\n-6\n7\n-8\n9\n-10\n11\n-12\n', result: (11,-12).",
        ),
        pytest.param(
            "11\n-12\n3\n-4\n5\n-6\n7\n-8\n9\n-10\n1\n-2\n",
            (-12, 11),
            id="'11\n-12\n3\n-4\n5\n-6\n7\n-8\n9\n-10\n1\n-2\n', result: (11,-12).",
        ),
        pytest.param(
            "\n".join(str(num) for num in range(0, 667000)),
            (0, 666999),
            id="Integers from 0 to 666999 delimited by '\n'.",
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
        assert find_maximum_and_minimum(file.name) == expected_result
