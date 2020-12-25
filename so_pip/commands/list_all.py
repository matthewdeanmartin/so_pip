"""
List packages
"""
import os
import shutil
from typing import List


def list_dirs(path:str)->List[str]:
    # https://stackoverflow.com/a/31049707/33264
    return [directory for directory in os.listdir(path)
            if os.path.isdir(os.path.join(path, directory))]

def list_packages(target_folder: str, quiet:bool=False) -> None:
    """List packages"""
    if not quiet:
        print(f"Using {target_folder} as vendorized folder")
    path = os.path.join(target_folder)
    for folder in list_dirs(path):
        # TODO: Add version
        print(folder)
