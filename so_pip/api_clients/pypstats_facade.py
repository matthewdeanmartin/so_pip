"""
What I really want to know is if a package exists and pypi's xmlrpc api's
are down today & at risk of going away altogether. The HTML API is ugly.

So I'm using a stats API. As a side effect, I can add a cut off for
unpopular packages.
"""

import json
from functools import lru_cache
from typing import List, Optional, Tuple

import pypistats

# endpoints
# -----------
# recent downloads
# ovarall downloads, broken down by mirrors
# major, minor, system, downloads by minor version, system, etc
import requests


def find_modules(
    module_list: List[str], minimum_downloads: int
) -> Tuple[List[str], List[str]]:
    """Assuming package exists of same name, see if it exists
    This is not true for a lot of packages.
    """
    packages_of_same_name: List[str] = []
    not_in_pypi: List[str] = []
    for module in module_list:
        downloads = get_download_count(module)

        if downloads and downloads > minimum_downloads:
            packages_of_same_name.append(module)
        else:
            not_in_pypi.append(module)
    return packages_of_same_name, not_in_pypi


@lru_cache(maxsize=1000)
def get_download_count(module: str) -> Optional[int]:
    """Get download count and cache it"""
    try:
        item_string = pypistats.overall(module.strip(), format="json")
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            return None
        raise
    # print(item_string)
    item = json.loads(item_string)
    downloads = None
    if isinstance(item, dict):
        for category in item["data"]:
            if "without_mirrors" in category.values():
                downloads = category["downloads"]
    return downloads
