"""
Unit tests for `merge_sorted_files`
from module `homework_9.tasks.task_1`.
"""
from pathlib import Path

from homework_9.tasks.task_1 import merge_sorted_files

# pylint: disable=unused-import
from homework_9.tests.fixtures import create_tmp_file, tmp_dir

# pylint: disable=redefined-outer-name


def test_single_file(create_tmp_file):
    """
    Passes test if `merge_sorted_files` works correctly
    on the one sorted file with integers per lines.
    """
    _1_3_5_lines_txt = create_tmp_file("1_3_5_lines.txt", "1\n3\n5\n")
    assert list(merge_sorted_files([_1_3_5_lines_txt])) == [1, 3, 5]


def test_multiple_files(create_tmp_file):
    """
    Passes test if `merge_sorted_files` works correctly
    on the sorted files with integers per lines.
    """
    _1_3_5_lines_txt = create_tmp_file("1_3_5_lines.txt", "1\n3\n5\n")
    _2_4_6_lines_txt = create_tmp_file("2_4_6_lines.txt", "2\n4\n6\n")
    files = [_1_3_5_lines_txt, Path(_2_4_6_lines_txt)]
    assert list(merge_sorted_files(files)) == [1, 2, 3, 4, 5, 6]


def test_empty_lines_file(create_tmp_file):
    """
    Passes test if `merge_sorted_files` yields
    nothing for the file with empty lines.
    """
    _3_empty_lines_txt = create_tmp_file("_3_empty_lines.txt", "\n\n\n")
    assert list(merge_sorted_files([_3_empty_lines_txt])) == []


def test_empty_file(create_tmp_file):
    """
    Passes test if `merge_sorted_files`
    yields nothing for the empty file.
    """
    empty_txt = create_tmp_file("empty.txt", "")
    assert list(merge_sorted_files([empty_txt])) == []


def test_repeated_integers(create_tmp_file):
    """
    Passes test if `merge_sorted_files`
    correctly merges repeated integers.
    """
    _1_3_5_lines_txt = create_tmp_file("1_3_5_lines.txt", "1\n3\n5\n")
    _2_5_6_lines_txt = create_tmp_file("2_5_6_lines.txt", "2\n5\n6\n")
    files = [_1_3_5_lines_txt, _2_5_6_lines_txt]
    assert list(merge_sorted_files(files)) == [1, 2, 3, 5, 5, 6]


def test_unsorted_integers(create_tmp_file):
    """
    Passes test if `merge_sorted_files` can
    not correctly merge unsorted integers.
    """
    _5_3_1_lines_txt = create_tmp_file("5_3_1_lines.txt", "5\n3\n1\n")
    _2_6_4_lines_txt = create_tmp_file("2_6_4_lines.txt", "2\n6\n4\n")

    files = [_5_3_1_lines_txt, _2_6_4_lines_txt]
    result = list(merge_sorted_files(files))
    assert result != [1, 2, 3, 4, 5, 6]
    assert result == [2, 5, 3, 1, 6, 4]
