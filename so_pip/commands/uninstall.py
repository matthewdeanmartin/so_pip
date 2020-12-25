"""
Uninstall command.

Tricky if using question id & answer id
"""
import os
import shutil


def uninstall_package(target_folder: str, package_name: str) -> None:
    """Clean out that old folder"""
    print(f"Using {target_folder} as location for vendorized packages.")
    path = os.path.join(target_folder, package_name)
    if not os.path.exists(path):
        print(f"WARNING: skipping {package_name} as it is not installed.")
        return
    shutil.rmtree(path)
    return
