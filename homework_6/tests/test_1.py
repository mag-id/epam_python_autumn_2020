"""Unit tests for `extended_wraps` decorator from module `homework_6.tasks.task_1`."""

from homework_6.tasks.task_1 import instances_counter


# pylint: disable=R0903 (too-few-public-methods)
class Helper:
    """Helper class."""


def test_methods_existence():
    """
    Passes test if `get_created_instances` and
    `reset_instances_counter` methods are exist in
    `DecoratedHelper` as well as in it `instance`.
    """
    DecoratedHelper = instances_counter(Helper)

    assert DecoratedHelper.get_created_instances
    assert DecoratedHelper.reset_instances_counter

    instance = DecoratedHelper()

    assert instance.get_created_instances
    assert instance.reset_instances_counter


def test_get_created_instances():
    """
    Passes test if the initial number of created `DecoratedHelper`
    instances are equal to 0 and final - to 1.
    """
    DecoratedHelper = instances_counter(Helper)

    no_instances = DecoratedHelper.get_created_instances()
    one_instance = DecoratedHelper().get_created_instances()

    assert (no_instances, one_instance) == (0, 1)


def test_reset_instances_counter():
    """
    Passes test if the initial number of created `DecoratedHelper` instances
    after first reset are equal to 1 and after second - to 0.
    """
    DecoratedHelper = instances_counter(Helper)

    one_instance = DecoratedHelper().reset_instances_counter()
    no_instances = DecoratedHelper.reset_instances_counter()

    assert (one_instance, no_instances) == (1, 0)


# pylint: disable=R0914 (too-many-locals)
def test_separate_decorating():
    """Passes test if decorated classes correspond to current behaviour."""

    class User:
        """Helper class."""

        def __init__(self, id_: str):
            self.id_ = id_

    class Admin(User):
        """Inherited helper class."""

    DecoratedUser = instances_counter(User)
    DecoratedAdmin = instances_counter(Admin)

    # Checks initial and created number of `DecoratedUser` instances.
    initial_user_instances = DecoratedUser.get_created_instances()
    user, _, _, = (
        DecoratedUser("1"),
        DecoratedUser("2"),
        DecoratedUser("3"),
    )
    created_user_instances = user.get_created_instances()

    assert (initial_user_instances, created_user_instances) == (0, 3)

    # Checks initial and created number of `DecoratedAdmin` instances.
    initial_admin_instances = DecoratedAdmin.get_created_instances()
    admin, _, _, = (
        DecoratedAdmin("1"),
        DecoratedAdmin("2"),
        DecoratedAdmin("3"),
    )
    created_admin_instances = admin.get_created_instances()

    assert (initial_admin_instances, created_admin_instances) == (0, 3)

    # Checks reset `DecoratedUser` and current `DecoratedAdmin` number of instances.
    reset_user_instances = user.reset_instances_counter()
    current_admin_instances = admin.get_created_instances()

    assert (reset_user_instances, current_admin_instances) == (3, 3)

    # Checks current `DecoratedUser` and reset `DecoratedAdmin` number of instances.
    reset_admin_instances = admin.reset_instances_counter()
    current_user_instances = user.get_created_instances()

    assert (current_user_instances, reset_admin_instances) == (0, 3)

    # Checks final `DecoratedUser` and `DecoratedAdmin` number of instances.
    final_admin_instances = admin.get_created_instances()
    final_user_instances = user.get_created_instances()

    assert (final_user_instances, final_admin_instances) == (0, 0)


# pylint: disable=no-member
def test_inherited_decorating():
    """Passes test if decorated classes correspond to current behaviour."""

    @instances_counter
    class DecoratedUser:
        """Helper class."""

        def __init__(self, id_: str):
            self.id_ = id_

    class DecoratedAdmin(DecoratedUser):
        """Inherited helper class."""

    # Checks initial and created number of `DecoratedUser` instances.
    initial_user_instances = DecoratedUser.get_created_instances()
    user, _, _, = (
        DecoratedUser("1"),
        DecoratedUser("2"),
        DecoratedUser("3"),
    )
    created_user_instances = user.get_created_instances()

    assert (initial_user_instances, created_user_instances) == (0, 3)

    # Checks initial and created number of `DecoratedAdmin` instances.
    initial_admin_instances = DecoratedAdmin.get_created_instances()
    admin, _, _, = (
        DecoratedAdmin("1"),
        DecoratedAdmin("2"),
        DecoratedAdmin("3"),
    )
    created_admin_instances = admin.get_created_instances()

    assert (initial_admin_instances, created_admin_instances) == (3, 6)

    # Checks reset `DecoratedUser` and current `DecoratedAdmin` number of instances.
    reset_user_instances = user.reset_instances_counter()
    current_admin_instances = admin.get_created_instances()

    assert (reset_user_instances, current_admin_instances) == (3, 6)

    # Checks current `DecoratedUser` and reset `DecoratedAdmin` number of instances.
    reset_admin_instances = admin.reset_instances_counter()
    current_user_instances = user.get_created_instances()

    assert (current_user_instances, reset_admin_instances) == (0, 6)

    # Checks final `DecoratedUser` and `DecoratedAdmin` number of instances.
    final_admin_instances = admin.get_created_instances()
    final_user_instances = user.get_created_instances()

    assert (final_user_instances, final_admin_instances) == (0, 0)
