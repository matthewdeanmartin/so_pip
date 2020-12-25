"""
List in requirements format.
"""
from so_pip.commands.list_all import list_packages


def freeze_environment(target_folder: str) -> None:
    """List packages and versions"""
    list_packages(target_folder, quiet=True)
