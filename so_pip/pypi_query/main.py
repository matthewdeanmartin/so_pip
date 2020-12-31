import os
from typing import List

import requests

from so_pip.utils.files_utils import find_file


class PackageInfo():
    def __init__(self):
        r = requests.get("https://pypi.python.org/simple/")
        r.raise_for_status()
        self.html_file = find_file("pypi.html", __file__)
        self.packages: List[str] = []
        if not os.path.exists("pypi.html"):
            with open(self.html_file, "w") as file:
                self.html_raw = r.text
                file.write(self.html_raw)
        else:
            with open(self.html_file, "r") as file:
                self.html_raw = file.read()
        self.html_lines = self.html_raw.split("\n")
        for line in self.html_lines:
            if "<a href=" not in line:
                continue
            package = line.split('>')[1].split("<")[0]
            self.packages.append(package)

    def search(self, package: str) -> bool:
        return package in self.packages


if __name__ == "__main__":
    p = PackageInfo()
    print(p.search("str"))
    print(p.search("bool"))
