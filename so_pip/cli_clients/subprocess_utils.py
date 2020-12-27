"""
Reduce friction of working with subproess
"""
import subprocess  # nosec
from typing import Dict, List, Optional


def execute_get_text(
    command: List[str],
    ignore_error: bool = False,
    # shell: bool = True, # causes cross plat problems, security warnings, etc.
    env: Optional[Dict[str, str]] = None,
) -> str:
    """
    Execute shell command and return stdout txt
    """

    completed = None
    try:
        completed = subprocess.run(  # nosec
            command,
            check=not ignore_error,
            # shell=shell, # causes cross plat problems, security warnings, etc.
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
    except subprocess.CalledProcessError:
        if ignore_error and completed:
            return completed.stdout.decode("utf-8") + completed.stderr.decode("utf-8")
        raise
    else:
        return completed.stdout.decode("utf-8") + completed.stderr.decode("utf-8")
