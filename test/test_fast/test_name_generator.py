import random

from so_pip.parse_python.make_name import make_up_module_name, number_from_name


def test_make_up_module_name() -> None:
    """exercise code"""
    for _ in range(0, 200):
        value = random.randint(1, 100000000)  # nosec
        module_name = make_up_module_name(value, "foo", "q")
        print(value, module_name, number_from_name(module_name))
        assert module_name
        assert number_from_name(module_name) == value
