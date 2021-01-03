"""
Uninstall command.

Tricky if using question id & post id
"""
import os
import shutil

from so_pip.utils import guards as guards
from so_pip.utils.user_trace import inform


def uninstall_package(target_folder: str, package_name: str) -> None:
    """Clean out that old folder"""
    guards.must_be_truthy(target_folder, "target_folder required")
    guards.must_be_truthy(package_name, "package_name required")
    inform(f"Using {target_folder} as location for vendorized packages.")
    path = os.path.join(target_folder, package_name)
    if not os.path.exists(path):
        print(f"WARNING: skipping {package_name} as it is not installed.")
        return
    shutil.rmtree(path)
    return
