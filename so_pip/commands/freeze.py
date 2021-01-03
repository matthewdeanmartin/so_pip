"""
List in requirements format.
"""
from so_pip.commands.list_all import list_packages
import so_pip.utils.guards as guards


def freeze_environment(target_folder: str) -> None:
    """List packages and versions"""
    guards.must_be_truthy(target_folder, "target_folder required")
    list_packages(target_folder, quiet=True)
