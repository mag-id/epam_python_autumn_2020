"""
Unit tests for module `homework_4.tasks.task_3`.
"""
import pytest

from homework_4.tasks.task_3 import my_precious_logger


@pytest.mark.parametrize(
    ["inp", "expected_out", "expected_err"],
    [
        pytest.param("OK", "OK", "", id="Common case: inp --> out."),
        pytest.param(
            "error: not found", "", "error: not found", id="Common case: inp --> err."
        ),
    ],
)
def test_common_cases_for_my_precious_logger(
    capsys, inp: str, expected_out: str, expected_err: str
):
    """
    Passes test if `my_precious_logger(inp)` write
    `expected_out` in `sys.stdout`, and `expected_err` in `sys.stderr`.
    """
    my_precious_logger(inp)
    our, err = capsys.readouterr()
    assert (our, err) == (expected_out, expected_err)


@pytest.mark.parametrize(
    ["inp", "expected_out", "expected_err"],
    [
        pytest.param("", "", "", id="Boundary case: empty inp --> empty out."),
        pytest.param(" ", " ", "", id="Boundary case: ' ' inp --> ' ' out."),
        pytest.param("0", "0", "", id="Boundary case: '0' inp --> '0' out."),
        pytest.param("1", "1", "", id="Boundary case: '1' inp --> '1' out."),
        pytest.param(
            "Error", "Error", "", id="Boundary case: 'Error' inp --> 'Error' out."
        ),
        pytest.param(
            " error", " error", "", id="Boundary case: ' error' inp --> ' error' out."
        ),
    ],
)
def test_boundary_cases_for_my_precious_logger(
    capsys, inp: str, expected_out: str, expected_err: str
):
    """
    Passes test if `my_precious_logger(inp)` write
    `expected_out` in `sys.stdout`, and `expected_err` in `sys.stderr`.
    """
    my_precious_logger(inp)
    our, err = capsys.readouterr()
    assert (our, err) == (expected_out, expected_err)
