"""
Unit tests for module `homework_2.tasks.task_1`.

Readable `CONTENT` in `UTF-8`:
------------------------------

E R N S T       J Ü N G E R
D E R     W A L D G A N G

»Jetzt und hier«

1

Der Waldgang — es ist keine Idylle, die sich hinter dem Titel
verbirgt.  Der  Leser  muß  sich  vielmehr  auf  einen  bedenkli-
chen Ausflug gefaßt machen, der nicht nur über vorgebahnte
Pfade, sondern auch über die Grenzen der Betrachtung hin-
ausführen wird.

Die Ja- und die Neinstimmen wer-
den verlesen — die einen mit wohlwollender, die anderen mit
bösartiger Befriedigung.

Das Wissen bildet nicht nur das symbolisch-
sakramentale  Fundament  der  Kirchen,  es  spinnt  sich  nicht
nur         in Geheimlehren und Sekten fort, sondern es stellt auch
den Kern der Philosopheme, wie überaus verschieden immer


deren Begriffswelt sei.

Erste Fassung Aufzeichnungen
bei Tag und Nacht

156 Seiten.

ISBN 3-608-93071-X

Schutzumschlag:
Autograph Ernst Jünger
(DLA. Marbach a. N.)

Punctuation characters = 30:
----------------------------
» « — , . - , , - . - - — , . - , , , . . - - - : ( . . . )

Non-ASCII characters = 13:
--------------------------
Ü » « — ß ß ü ü ü — ö ü ü
"""

# pylint: disable=redefined-outer-name
# ^^^ this

from typing import List

import pytest

from homework_2.tasks.task_1 import (
    count_non_ascii_chars,
    count_punctuation_chars,
    get_longest_diverse_words,
    get_most_common_non_ascii_char,
    get_rarest_char,
)

CONTENT = """E R N S T       J \u00dc N G E R
D E R     W A L D G A N G

\u00bbJetzt und hier\u00ab

1

Der Waldgang \u2014 es ist keine Idylle, die sich hinter dem Titel
verbirgt.  Der  Leser  mu\u00df  sich  vielmehr  auf  einen  bedenkli-
chen Ausflug gefa\u00dft machen, der nicht nur \u00fcber vorgebahnte
Pfade, sondern auch \u00fcber die Grenzen der Betrachtung hin-
ausf\u00fchren wird.

Die Ja- und die Neinstimmen wer-
den verlesen \u2014 die einen mit wohlwollender, die anderen mit
b\u00f6sartiger Befriedigung.

Das Wissen bildet nicht nur das symbolisch-
sakramentale  Fundament  der  Kirchen,  es  spinnt  sich  nicht
nur         in Geheimlehren und Sekten fort, sondern es stellt auch
den Kern der Philosopheme, wie \u00fcberaus verschieden immer


deren Begriffswelt sei.

Erste Fassung Aufzeichnungen
bei Tag und Nacht

156 Seiten.

ISBN 3-608-93071-X

Schutzumschlag:
Autograph Ernst J\u00fcnger
(DLA. Marbach a. N.)
"""


@pytest.fixture()
def filepath(tmp_path):
    """
    Returns temporary file path to file with `CONTENT`.
    """
    test_dir = tmp_path / "tmp_dir"
    test_dir.mkdir()
    test_data = test_dir / "test_data.txt"
    test_data.write_text(CONTENT, encoding="unicode_escape")
    return test_data


@pytest.mark.parametrize(
    [
        "expected_result",
    ],
    [
        pytest.param(
            [
                "symbolischsakramentale",
                "Schutzumschlag",
                "Aufzeichnungen",
                "hinausführen",
                "Begriffswelt",
                "vorgebahnte",
                "Betrachtung",
                "bedenklichen",
                "Philosopheme",
                "Befriedigung",
            ],
        ),
    ],
)
def test_get_longest_diverse_words(filepath, expected_result: List[str]):
    """
    Passes test if `get_longest_diverse_words`(`filepath`) is
    equal to `expected_result` where `filepath` is temporary
    file with `CONTENT`.
    """
    assert get_longest_diverse_words(filepath) == expected_result


@pytest.mark.parametrize(
    [
        "expected_result",
    ],
    [
        pytest.param(
            ["(", ")", "5", "7", "8", "9", ":", "M", "X", "«", "»", "Ü", "ö"],
        ),
    ],
)
def test_get_rarest_char(filepath, expected_result: List[str]):
    """
    Passes test if `get_rarest_char`(`filepath`) is
    equal to `expected_result` where `filepath` is temporary
    file with `CONTENT`.
    """
    assert get_rarest_char(filepath) == expected_result


@pytest.mark.parametrize(
    [
        "expected_result",
    ],
    [pytest.param(30)],
)
def test_count_punctuation_chars(filepath, expected_result: int):
    """
    Passes test if `count_punctuation_chars`(`filepath`) is
    equal to `expected_result` where `filepath` is temporary
    file with `CONTENT`.
    """
    assert count_punctuation_chars(filepath) == expected_result


@pytest.mark.parametrize(
    [
        "expected_result",
    ],
    [pytest.param(13)],
)
def test_count_non_ascii_chars(filepath, expected_result: int):
    """
    Passes test if `count_non_ascii_chars`(`filepath`) is
    equal to `expected_result` where `filepath` is temporary
    file with `CONTENT`.
    """
    assert count_non_ascii_chars(filepath) == expected_result


@pytest.mark.parametrize(
    [
        "expected_result",
    ],
    [pytest.param(["ü"])],
)
def test_get_most_common_non_ascii_char(filepath, expected_result: List[str]):
    """
    Passes test if `get_most_common_non_ascii_char`(`filepath`) is
    equal to `expected_result` where `filepath` is temporary
    file with `CONTENT`.
    """
    assert get_most_common_non_ascii_char(filepath) == expected_result
