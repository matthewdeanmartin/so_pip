"""
List packages
"""
import os
from typing import List

from so_pip.utils import guards as guards
from so_pip.utils.user_trace import inform


def list_dirs(path: str) -> List[str]:
    """Get list of directories"""
    # https://stackoverflow.com/a/31049707/33264
    guards.must_be_truthy(path, "path required")
    return [
        directory
        for directory in os.listdir(path)
        if os.path.isdir(os.path.join(path, directory))
    ]


def list_packages(target_folder: str, quiet: bool = False) -> None:
    """List packages"""
    guards.must_be_truthy(target_folder, "target_folder required")
    if not quiet:
        inform(f"Using {target_folder} as vendorized folder")
    path = os.path.join(target_folder)
    for folder in list_dirs(path):
        # TODO: Add version
        print(folder)
