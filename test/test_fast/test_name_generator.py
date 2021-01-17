import random

from so_pip.random_names.make_name import (
    make_up_module_name,
    number_from_name,
    initialize,
)


def test_make_up_module_name() -> None:
    """exercise code"""
    for _ in range(0, 200):
        value = random.randint(1, 100000000)  # nosec
        module_name = make_up_module_name(value, "foo", "q")
        print(value, module_name, number_from_name(module_name))
        assert module_name
        assert number_from_name(module_name) == value

        # should be invariant
        second = make_up_module_name(value, "foo", "q")
        third = make_up_module_name(value, "foo", "q")
        assert second == third


def test_make_up_module_name_reinitialize() -> None:
    """exercise code"""

    for _ in range(0, 200):
        initialize()
        value = random.randint(1, 100000000)  # nosec
        module_name = make_up_module_name(value, "foo", "q")
        print(value, module_name, number_from_name(module_name))
        assert module_name
        assert number_from_name(module_name) == value

        # should be invariant
        second = make_up_module_name(value, "foo", "q")
        initialize()
        third = make_up_module_name(value, "foo", "q")
        initialize()
        assert second == third
