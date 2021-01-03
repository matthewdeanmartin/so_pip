"""
Guess a language based on shebang
"""

# http://dcjtech.info/topic/list-of-shebang-interpreter-directives/
from typing import List

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
