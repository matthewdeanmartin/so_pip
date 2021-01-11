"""
Scrape twitter & github urls

https://stackapps.com/questions/7549/
how-can-i-get-user-links-in-the-api-call-like-twitter-github-and-so-on
"""
from functools import lru_cache
from typing import Tuple

import requests
from bs4 import BeautifulSoup


@lru_cache(maxsize=1000)
def scrape_urls(user_id: int) -> Tuple[str, str]:
    """Get twiter and github"""
    response = requests.get(f"https://stackoverflow.com/users/{user_id}/")
    if response.status_code != 200:
        return "", ""
    soup = BeautifulSoup(response.text, features="html.parser")
    twitter = ""
    github = ""
    for anchor in soup.findAll("a"):
        if "href" in anchor.attrs:
            candidate = anchor.attrs["href"]
            if (
                "twitter.com" in candidate
                and candidate != "https://twitter.com/stackoverflow"
            ):
                twitter = candidate
            if "github.com" in candidate:
                github = candidate
        # other URL we can get from API
        if twitter and github:
            return twitter, github
    return twitter, github


# print(scrape_urls(2145778))
