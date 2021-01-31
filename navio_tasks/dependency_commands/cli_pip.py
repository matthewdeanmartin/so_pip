"""
Register scripts
"""
import os
import shlex
import sys

from navio_tasks.cli_commands import (
    check_command_exists,
    config_pythonpath,
    execute,
    execute_with_environment,
    execute_get_text,
)
from navio_tasks.settings import (
    PIPENV_ACTIVE,
    PROJECT_NAME,
    VENV_SHELL,
    PIP_CHECK_SKIPS,
)
from navio_tasks.utils import inform


def do_register_scripts() -> None:
    """
    Without this console_scripts in the entrypoints section of setup.py aren't
    available
    :return:
    """
    check_command_exists("pip")

    # This doesn't work, it can't tell if "install -e ." has already run
    if dist_is_editable():
        inform("console_scripts already registered")
        return
    # install in "editable" mode
    command_text = f"{VENV_SHELL} pip install -e ."
    inform(command_text)
    command_text = command_text.strip().replace("  ", " ")
    command = shlex.split(command_text)
    execute(*command)


def dist_is_editable() -> bool:
    """Is distribution an editable install?"""
    for path_item in sys.path:
        egg_link = os.path.join(path_item, PROJECT_NAME + ".egg-link")
        if os.path.isfile(egg_link):
            return True
    return False


def do_pip_check() -> str:
    """
    Call as normal function
    """

    # TODO
    result = execute_get_text(
        command=["pip", "check"], ignore_error=True, env=config_pythonpath()
    )
    problems = []
    if PIP_CHECK_SKIPS:
        print(f"Ignoring pip incompat problems for : {PIP_CHECK_SKIPS}")
    for line in result.split("\n"):
        if not line.strip():
            continue
        for skip in PIP_CHECK_SKIPS:
            if skip in line:
                pass
            else:
                problems.append(line)
    if problems:
        for problem in problems:
            print(problem)
        print("pip check problems, even after skips")
        sys.exit(-1)

    environment = config_pythonpath()
    environment["PIPENV_PYUP_API_KEY"] = ""
    if PIPENV_ACTIVE:
        # ignore 38414 until aws fixes awscli
        execute_with_environment("pipenv check --ignore 38414", environment)
    return "Pip(env) check run"
