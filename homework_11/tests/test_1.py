"""
Unit tests for `SimplifiedEnum` from
module `homework_11.tasks.task_1`.
"""
import pytest

from homework_11.tasks.task_1 import INVALID_KEY, SimplifiedEnum

# pylint: disable=too-few-public-methods


class TestPositiveCases:
    """Wraps tests for positive cases."""

    @staticmethod
    def test_classes_naming():
        """
        Passes test if classes names are recognized.
        """

        # pylint: disable=no-member
        # pylint: disable=missing-class-docstring

        class PublicClass(metaclass=SimplifiedEnum):
            __keys = ("public",)

        class _ProtectedClass(metaclass=SimplifiedEnum):
            __keys = ("protected",)

        # pylint: disable=invalid-name
        class __PrivateClass(metaclass=SimplifiedEnum):
            __keys = ("private",)

        assert PublicClass.public == "public"
        assert _ProtectedClass.protected == "protected"
        assert __PrivateClass.private == "private"

    @staticmethod
    def test_iterable_containers():
        """
        Passes test if classes work predictably
        with different iterable `__keys` containers.
        """

        # pylint: disable=no-member
        # pylint: disable=missing-class-docstring

        class TupleContainer(metaclass=SimplifiedEnum):
            __keys = ("one", "two")

        class ListContainer(metaclass=SimplifiedEnum):
            __keys = ["one", "two"]

        class SetContainer(metaclass=SimplifiedEnum):
            __keys = {"one", "two"}

        class SetFrozenContainer(metaclass=SimplifiedEnum):
            __keys = frozenset(["one", "two"])

        class DictContainer(metaclass=SimplifiedEnum):
            __keys = {"one": 1, "two": 2}

        expected_result = "one", "two"
        assert (TupleContainer.one, TupleContainer.two) == expected_result
        assert (ListContainer.one, ListContainer.two) == expected_result
        assert (SetContainer.one, SetContainer.two) == expected_result
        assert (SetFrozenContainer.one, SetFrozenContainer.two) == expected_result
        assert (DictContainer.one, DictContainer.two) == expected_result

    @staticmethod
    def test_empty_container():
        """
        Passes test if a class with an empty
        container has not any attributes.
        """

        # pylint: disable=no-member
        # pylint: disable=missing-class-docstring

        class EmptyContainer(metaclass=SimplifiedEnum):
            __keys = []

        assert list(EmptyContainer) == []


class TestNegativeCases:
    """Wraps tests for negative cases."""

    @staticmethod
    @pytest.mark.parametrize(
        ["key"],
        [
            # bool-s
            pytest.param(False, id="False"),
            pytest.param(True, id="True"),
            # int-s
            pytest.param(0, id="0"),
            pytest.param(1, id="1"),
            # str-s
            pytest.param("", id="''"),
            pytest.param(" ", id="' '"),
            pytest.param(".", id="'.'"),
            pytest.param("*", id="'*'"),
            pytest.param("+", id="'+'"),
            pytest.param("\n", id="'\\n'"),
            pytest.param("\\n", id="'\\\n'"),
            pytest.param("one two", id="'one two'"),
            # pytest.param("_", id="'_'"), ?
        ],
    )
    def test_wrong_string_keys(key: str):
        """
        Passes test if invalid key
        raises `ValueError(INVALID_KEY)`
        """

        # pylint: disable=no-member
        # pylint: disable=missing-class-docstring

        with pytest.raises(ValueError, match=INVALID_KEY):

            class EmptyContainer(metaclass=SimplifiedEnum):
                __keys = (key,)

            _ = EmptyContainer
