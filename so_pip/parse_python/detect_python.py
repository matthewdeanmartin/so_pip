"""
Fast detect python.

https://github.com/TomCrypto/Codex/blob/master/codex.py
"""
import re


def _compiled_regex(pattern, dotall=True):
    flags = (re.MULTILINE | re.DOTALL) if dotall else re.MULTILINE
    return re.compile(pattern, flags)


MARKERS = [
    # Python markers
    _compiled_regex(
        r"^(\s*from\s+[\.\w]+)?\s*import\s+[\*\.,\w]+(,\s*[\*\.,\w]+)*(\s+as\s+\w+)?$"
    ),
    _compiled_regex(r"^\s*def\s+\w+\((.*?):$", dotall=True),
    _compiled_regex(r"^\s*if\s(.*?):$(.*?)(^\s*else:)?$", dotall=False),
    _compiled_regex(r"^\s*if\s(.*?):$(.*?)(^\s*elif:)?$", dotall=False),
    _compiled_regex(r"^\s*try:$(.*?)^\s*except(.*?):"),
    _compiled_regex(r"True|False"),
    _compiled_regex(r"==\s*(True|False)"),
    _compiled_regex(r"is\s+(None|True|False)"),
    _compiled_regex(r"^\s*if\s+(.*?)\s+in[^:\n]+:$", dotall=False),
    _compiled_regex(r"^\s*pass$"),
    _compiled_regex(r"print\((.*?)\)$", dotall=False),
    _compiled_regex(r"^\s*for\s+\w+\s+in\s+(.*?):$"),
    _compiled_regex(r"^\s*class\s+\w+\s*(\([.\w]+\))?:$", dotall=False),
    _compiled_regex(r"^\s*@(staticmethod|classmethod|property)$"),
    _compiled_regex(r"__repr__"),
    _compiled_regex(r'"(.*?)"\s+%\s+(.*?)$', dotall=False),
    _compiled_regex(r"'(.*?)'\s+%\s+(.*?)$", dotall=False),
    _compiled_regex(r"^\s*raise\s+\w+Error(.*?)$"),
    _compiled_regex(r'"""(.*?)"""'),
    _compiled_regex(r"'''(.*?)'''"),
    _compiled_regex(r"\s*# (.*?)$"),
    _compiled_regex(r"^\s*import re$"),
    _compiled_regex(r"re\.\w+"),
    _compiled_regex(r"^\s*import time$"),
    _compiled_regex(r"time\.\w+"),
    _compiled_regex(r"^\s*import datetime$"),
    _compiled_regex(r"datetime\.\w+"),
    _compiled_regex(r"^\s*import random$"),
    _compiled_regex(r"random\.\w+"),
    _compiled_regex(r"^\s*import math$"),
    _compiled_regex(r"math\.\w+"),
    _compiled_regex(r"^\s*import os$"),
    _compiled_regex(r"os\.\w+"),
    _compiled_regex(r"^\s*import os.path$"),
    _compiled_regex(r"os\.path\.\w+"),
    _compiled_regex(r"^\s*import sys$"),
    _compiled_regex(r"sys\.\w+"),
    _compiled_regex(r"^\s*import argparse$"),
    _compiled_regex(r"argparse\.\w+"),
    _compiled_regex(r"^\s*import subprocess$"),
    _compiled_regex(r"subprocess\.\w+"),
    _compiled_regex(r'^\s*if\s+__name__\s*=\s*"__main__"\s*:$'),
    _compiled_regex(r"^\s*if\s+__name__\s*=\s*'__main__'\s*:$"),
    _compiled_regex(r"self\.\w+(\.\w+)*\((.*?)\)"),
]


def score(text: str) -> int:
    """Count features that signal python, multiples
    worth extra only for 2nd."""
    so_far = 0
    for finder in MARKERS:
        found = finder.findall(text)
        so_far += len(found) if len(found) < 3 else 2
        # print(finder.pattern, found)
    return so_far


if __name__ == "__main__":
    print(score(open(__file__).read()))
