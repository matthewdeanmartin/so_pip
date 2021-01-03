"""
Utility functions to help with code coverage.

Imagine:

def foo(bar):
    if bar is None:
        raise Exception()

Hitting the guard requires an extra unit test and provides little
value to get 100% coverage. (And to hit 90% coverage, you need to
have 100% coverage on most files)
"""
import logging
from typing import Any, Dict

LOGGER = logging.getLogger(__name__)


def must_not_be_none(value: Any, message: str = "Value must not be none") -> None:
    """
    Raise exception if value is None
    """
    if value is None:
        LOGGER.error(f"Can't be none, but got {value}")
        raise TypeError(message)


def must_not_be_truthy(value: bool, message: str = "Value must not be truthy") -> None:
    """
    Guard to assert truthiness & make it easier to get unit test coverage.
    """
    if value:
        LOGGER.error(f"Can't be truthy, but got {value}")
        raise TypeError(message)


def must_be_truthy(value: Any, message: str = "Value must not be truthy") -> None:
    """
    Guard to assert truthiness & make it easier to get unit test coverage.
    """
    if not value:
        LOGGER.error(f"Must be truthy, but got {value}")
        raise TypeError(message)


def must_not_be_falsy(value: Any, message: str = "Value must not be falsy") -> None:
    """
    Raise exception if value is falsy (i.e. False, "", None, [], etc)
    """
    if not value:
        LOGGER.error(f"Must not be falsy, but got {value}")
        raise TypeError(message)


def must_be_falsy(value: Any, message: str = "Value must not be falsy") -> None:
    """
    Raise exception if value is not falsy (i.e. False, "", None, [], etc)
    """
    if value:
        LOGGER.error(f"Must be falsy, but got {value}")
        raise TypeError(message)


def must_not_already_be_in_dictionary(
    key: Any,
    dictionary: Dict[Any, Any],
    message: str = "Key already in dictionary",
    warn_only: bool = False,
) -> None:
    """Assert we aren't about to insert a key twice to a dict"""
    if key in dictionary:
        if warn_only:
            print(
                f"{key} is already in dictionary where it has "
                f"a value of {dictionary[key]}"
            )
        else:
            raise TypeError(message)


def assert_is_number(value: str) -> None:
    """
    Raise error if there is a value and the value is not a number
    """
    if value is None:
        # Why did I do this?
        return
    # pylint: disable=broad-except
    # noinspection PyBroadException
    try:
        _ = int(value)
    except BaseException:
        LOGGER.error(f"Expected numerical id, got {value}")
