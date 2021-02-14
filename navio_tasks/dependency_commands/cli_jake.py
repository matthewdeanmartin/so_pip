"""
Same as safety but managed by a different company. Probably a different
vulnerability database. Can integrate with on prem somatype server if available.

Only reports
No file changes
Should break build on any issues.
Expect few issues
All issues should be addressable immediately.
"""
import shlex

from navio_tasks.cli_commands import check_command_exists, execute
from navio_tasks.settings import VENV_SHELL
from navio_tasks.utils import inform


def do_jake() -> str:
    """
    Check free database for vulnerabilities in active venv.
    """
    # TODO: get an API key and start using
    #  .oss-index-config
    command_name = "jake"
    check_command_exists(command_name)

    command_text = f"{VENV_SHELL} {command_name} ddt".strip().replace("  ", " ")
    inform(command_text)
    command = shlex.split(command_text)
    execute(*command)
    return "jake succeeded"
