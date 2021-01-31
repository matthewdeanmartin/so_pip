"""
Check if package even exists
"""
import os
from functools import lru_cache
from typing import List, Tuple

import requests

from so_pip.utils.files_utils import find_file

PYPI = None


def find_modules(module_list: List[str]) -> Tuple[List[str], List[str]]:
    """Assuming package exists of same name, see if it exists
    This is not true for a lot of packages.
    """
    packages_of_same_name: List[str] = []
    not_in_pypi: List[str] = []
    for module in module_list:
        # The API runs into rate limits
        # downloads = get_download_count(module)
        # downloads and downloads > minimum_downloads:
        if package_exists(module):
            packages_of_same_name.append(module)
        else:
            not_in_pypi.append(module)
    return packages_of_same_name, not_in_pypi


@lru_cache(maxsize=1000)
def package_exists(module: str) -> bool:
    """Get download count and cache it"""
    # pylint: disable=global-statement
    global PYPI
    if not PYPI:
        PYPI = PackageInfo()
    return PYPI.search(module)


class PackageInfo:
    """Stateful way to load and parse the data file"""

    def __init__(self) -> None:
        """Fire up initial state"""
        self.html_file = find_file("../_cache/pypi.html", __file__)
        self.packages: List[str] = []
        if not os.path.exists(self.html_file):
            client = requests.get("https://pypi.python.org/simple/")
            client.raise_for_status()
            with open(self.html_file, "w") as file:
                self.html_raw = client.text
                file.write(self.html_raw)
        else:
            with open(self.html_file) as file:
                self.html_raw = file.read()
        self.html_lines = self.html_raw.split("\n")
        for line in self.html_lines:
            if "<a href=" not in line:
                continue
            package = line.split(">")[1].split("<")[0]
            self.packages.append(package)

    def search(self, package: str) -> bool:
        """Check if package exists"""
        return package.strip() in self.packages
