"""
Convert a post id to a english name in a hopefully reversible manner
"""

# word list ultimately from wictionary
# https://www.wordexample.com/list/most-common-nouns-english
from typing import Any, List

from so_pip.utils.files_utils import find_file

NAMES: List[str] = []

FILE = "clean_ten_k.txt"


def initialize() -> None:
    """Read name file lazily"""
    if NAMES:
        return

    # words_path = find_file("most-common-nouns-english.csv",__file__)
    # source: https://www.mit.edu/~ecprice/wordlist.10000
    # See ETL for what it took to get a clean file.
    words_path = find_file(FILE, __file__)
    with open(words_path) as name_file:
        NAMES.extend(list(name.strip() for name in name_file.readlines()))

    if len(NAMES) != 10000:
        raise TypeError(f"Init failed, didn't find 10,000 words, got {len(NAMES)}")


# TODO: replace with a SO sourced post.
# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(value: List[Any], number: int) -> Any:
    """ looping till length l"""
    for index in range(0, len(value), number):
        yield value[index : index + number]


def number_from_name(name: str) -> int:
    """Convert name into number"""
    initialize()
    if "_q_" in name:
        generated_part = name.split("_q_")
    elif "_a_" in name:
        generated_part = name.split("_a_")
    else:
        raise TypeError("Needs _q_ or _a_ to split prefix from generated name")

    parts = generated_part[1].split("_")
    if len(parts) == 1:
        index = NAMES.index(parts[0])
        return index
    if len(parts) == 2:
        index = NAMES.index(parts[1]) * 10000
        index += NAMES.index(parts[0])
        return index
    if len(parts) == 3:
        index = NAMES.index(parts[2]) * 10000 * 10000
        index += NAMES.index(parts[1]) * 10000
        index += NAMES.index(parts[0])
        return index
    raise TypeError("Don't know how ot deal with numbers this big.")


def make_up_module_name(value: int, prefix: str, post_type: str) -> str:
    """Convert number into repeatable random name"""
    initialize()
    parts = []
    # posts                            65,448,638 ~ 2021, 10 years worth
    # 1000 means ~ 3 word names for 1,000,000,000, 1 billion
    # 10000 means ~ 2 words for       100,000,000, 100 million
    for chunk in divide_chunks(list(reversed(str(value))), 4):
        index = int("".join(list(reversed(chunk))))
        parts.append(NAMES[index])
    return "_".join([prefix, post_type] + parts)
