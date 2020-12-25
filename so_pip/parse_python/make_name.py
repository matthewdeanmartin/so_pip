"""
Convert a post id to a english name in a hopefully reversable manner
"""

# word list ultimately from wictionary
# https://www.wordexample.com/list/most-common-nouns-english
import random
from typing import Any, List

from so_pip.file_writing import find_file

NAMES: List[str] = []


def initialize() -> None:
    """Read name file lazily"""
    if NAMES:
        return

    # words_path = find_file("most-common-nouns-english.csv",__file__)
    # source: https://www.mit.edu/~ecprice/wordlist.10000
    words_path = find_file("wordlist.10000.txt", __file__)
    with open(words_path) as name_file:
        raw_names = [name.strip() for name in name_file.readlines()]

    for name in raw_names:
        if "Word" in name:
            continue
        if "," in name:
            NAMES.append(name.split(",")[0])
        else:
            NAMES.append(name)
    if len(NAMES) != 10000:
        raise TypeError("Init failed, didn't find 10,000 words.")


# TODO: replace with a SO sourced answer.
# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(value: List[Any], number: int) -> Any:
    """ looping till length l"""
    for index in range(0, len(value), number):
        yield value[index : index + number]


def make_up_module_name(value: int) -> str:
    """Convert number into repeatable random name"""
    initialize()
    parts = []
    # posts                            65,448,638 ~ 2021, 10 years worth
    # 1000 means ~ 3 word names for 1,000,000,000, 1 billion
    # 10000 means ~ 2 words for       100,000,000, 100 million
    for chunk in divide_chunks(list(reversed(str(value))), 4):
        index = int("".join(list(reversed(chunk))))
        parts.append(NAMES[index])
    return "_".join(parts)


if __name__ == "__main__":

    def run() -> None:
        """exercise code"""
        for _ in range(0, 200):
            value = random.randint(1, 100000000)  # nosec
            print(make_up_module_name(value))

    run()
