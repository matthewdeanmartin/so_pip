"""
Plain web scraper
"""
import pprint
from typing import Any

from search_engine_parser.core.engines.stackoverflow import Search


def search_string(query: str) -> Any:
    """
    This is likely to fail unless you are on a brand new IP, and even then, it might
    fail. SO doesn't like screen scrapers.
    """
    search_args = (query, 1)
    engine = Search()
    results = engine.search(*search_args)
    return results


if __name__ == "__main__":

    def run() -> None:
        results = search_string(query="[python] is:answer def class aws")
        for result in results:
            pprint.pprint(result)
