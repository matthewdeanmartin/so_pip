"""
Fast detect python.

https://github.com/TomCrypto/Codex/blob/master/codex.py
"""
import re
from typing import List


def _compiled_regex(pattern: str, dotall: bool = True) -> re.Pattern:
    """precompile some regex"""
    flags = (re.MULTILINE | re.DOTALL) if dotall else re.MULTILINE
    return re.compile(pattern, flags)


MARKERS: List[re.Pattern] = [
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


# http://dcjtech.info/topic/list-of-shebang-interpreter-directives/
SHEBANGS = {
    "#!/usr/bin/python": ".py",
    "#!/usr/bin/env python": ".py",
    "#!/usr/bin/env python3": ".py",
    "#!/bin/ash": ".ash",
    "#!/usr/bin/awk": ".awk",
    "#!/bin/bash": ".sh",
    "#!/usr/bin/env bash": ".sh",
    "#!/bin/busybox sh": ".sh",
    "#!/bin/csh": ".csh",  # right extension?
    "#!/usr/local/bin/groovy": ".groovy",
    "#!/usr/bin/env groovy": ".groovy",
    "#!/usr/bin/env jsc": ".js",
    "#!/usr/bin/env node": ".js",
    "#!/usr/bin/env rhino": ".js",
    "#!/usr/local/bin/sbcl --script": ".lisp",
    "#!/usr/bin/env lua": ".lua",
    "#!/usr/bin/lua": ".lua",
    "#!/usr/bin/make -f": ".make",
    "#!/usr/bin/env perl": ".pl",
    "#!/usr/bin/perl": ".pl",
    "#!/usr/bin/perl -T": ".pl",
    "#!/usr/bin/php": ".php",
    "#!/usr/bin/env php": ".php",
    "#!/usr/bin/env ruby": ".rb",
    "#!/usr/bin/ruby": ".rb",
    "#!/bin/sed -f": ".sed",
    "#!/usr/bin/sed -f": ".sed",
    "#!/usr/bin/env sed": ".sed",
    "#!/bin/sh": ".sh",
    "#!/usr/xpg4/bin/sh": ".sh",
    "#!/bin/tcsh": ".tcsh",
}


def language_by_shebang(test: str) -> List[str]:
    """Identify by shebang"""
    possibles = set()
    for key, value in SHEBANGS.items():
        if key in test:
            possibles.add(value)
        if key.strip("#!/") in test:
            possibles.add(value)

    return list(possibles)


if __name__ == "__main__":
    print(score(open(__file__).read()))
