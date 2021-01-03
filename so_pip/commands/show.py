"""
List meta data for one.

# pkginfo 1.6.1
"""

# TODO: probably just extract metadata from __init__.py
import os

from so_pip.utils import guards as guards
from so_pip.utils.user_trace import inform


def show(target_folder: str, package_name: str) -> None:
    """Show pip style metadata"""
    guards.must_be_truthy(target_folder, "target_folder required")
    guards.must_be_truthy(package_name, "package_name required")
    package_path = os.path.join(target_folder, package_name)
    init_path = os.path.join(target_folder, package_name, "__init__.py")
    with open(init_path) as meta:
        for line in meta:
            if "Author Link:" in line:
                contact = line.split(":")[1].strip()
            if "Url:" in line:
                homepage = line.split(":")[1].strip()
            if "__" in line and "=" in line:
                if "version" in line:
                    version = line.split("=")[1].strip("'\"")
                if "license" in line:
                    the_license = line.split("=")[1].strip("'\"")
                if "author" in line:
                    author = line.split("=")[1].strip("'\"")
                if "title" in line:
                    title = line.split("=")[1].strip("'\"")
    requirements_path = os.path.join(target_folder, package_name, "requirements.txt")
    requirements = []
    if os.path.exists(requirements_path):
        with open(requirements_path) as requirements_file:
            for line in requirements_file:
                requirements.append(line)

    inform(f"Name: {package_name}")
    inform(f"Version: {version}")
    inform(f"Summary: {title}")
    inform(f"Home-page: {homepage}")
    inform(f"Author: {author}")
    inform(f"Author-email: {contact}")
    inform(f"License: {the_license}")
    inform(f"Location: {package_path}")
    inform(f"Requires: {','.join(requirements)}")
    inform("Required-by: N/A")
