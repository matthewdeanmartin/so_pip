# wordlist utlimately from wictionary
# https://www.wordexample.com/list/most-common-nouns-english
import random
from typing import Generator, Any, List, Iterator

from so_pip.file_writing import find_file

NAMES=[]

def initialize()->None:
    """Read name file lazily"""
    if NAMES:
        return
    words_path = find_file("most-common-nouns-english.csv",__file__)
    with open(words_path) as name_file:
        raw_names =[name.strip() for name in  name_file.readlines()]

    for name in raw_names:
        if "Word" in name:
            continue
        if "," in name:
            NAMES.append(name.split(",")[0])
        else:
            NAMES.append(name)
    assert len(NAMES) ==1000

# TODO: replace with a SO sourced answer.
# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(value:List[Any], number:int)->Any:
    """ looping till length l"""
    for index in range(0, len(value), number):
        yield value[index:index + number]

def make_up_module_name(value:int)->str:
    """Convert number into repeatable random name"""
    initialize()
    parts = []
    for chunk in divide_chunks(list(reversed(str(value))),3):
        index = int("".join(list(reversed(chunk))))
        parts.append(NAMES[index])
    return "_".join(parts)

if __name__ == "__main__":
    for i in range(0, 200):
        value = random.randint(1, 100000000)
        print(make_up_module_name(value))
