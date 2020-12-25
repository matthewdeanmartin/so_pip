"""
List meta data for one.

# pkginfo 1.6.1
"""

# TODO: probably just extract metadata from __init__.py
import os


def show(target_folder:str, package_name)->None:
    """Show pip style metadata"""
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
                    title =  line.split("=")[1].strip("'\"")
    requirements_path = os.path.join(target_folder, package_name, "requirements.txt")
    requirements = []
    if os.path.exists(requirements_path):
        with open(requirements_path) as requirements_file:
            for line in requirements_file:
                requirements.append(line)

    print(f"Name: {package_name}")
    print(f"Version: {version}")
    print(f"Summary: {title}")
    print(f"Home-page: {homepage}")
    print(f"Author: {author}")
    print(f"Author-email: {contact}")
    print(f"License: {the_license}")
    print(f"Location: {package_path}")
    print(f"Requires: {','.join(requirements)}")
    print(f"Required-by: N/A")

"""
__title__ = 'example function in Python: counting words'
__version__ = '1.0.1'
__author__ = 'eumiro'
__license__ = 'CC BY-SA 2.5'
__copyright__ = 'Copyright 2010-10-08 17:04:40 by eumiro'
"""
