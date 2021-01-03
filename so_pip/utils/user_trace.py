"""
Output for user to see.
"""
from so_pip import settings as settings


def inform(value: str) -> None:
    """(Pretty) print progress"""
    if not settings.QUIET:
        print(value)
