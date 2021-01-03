"""
Build tasks
"""
import configparser
import functools
import glob
import hashlib
import io
import json
import multiprocessing
import os
import platform
import re
import shlex
import shutil
import socket
import subprocess
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast

import setuptools

# on some shells print doesn't flush!
# pylint: disable=redefined-builtin,invalid-name
print = functools.partial(print, flush=True)

try:
    from pynt import task
    from pyntcontrib import execute, safe_cd

except ModuleNotFoundError:
    if hasattr(sys, "real_prefix"):
        print(
            "Pynt is not installed, run pipenv install --dev --skip-lock or poetry"
            "install"
        )
    else:
        print("Virtual environment not activated")
        print(
            "Either activate a virtual environment, or if this is docker, install"
            " dependencies with pip install -r requirements-dev.txt"
        )
    sys.exit(-1)

try:
    import dodgy.run as dodgy_runner
    import psutil
    import requests
    from checksumdir import dirhash
    from dotenv import load_dotenv
    from git import Repo
    from pebble import ProcessPool

except ModuleNotFoundError:
    print(
        "Activate pipenv or run pipenv install python-dotenv requests dodgy --skip-lock"
    )
    sys.exit(-1)

if os.path.exists(".env"):
    load_dotenv()


def check_public_ip(ipify: str = "https://api6.ipify.org/") -> str:
    """
    Try to get the elastic IP for this machine
    :rtype: str
    """
    # BUG: When this fails, it doesn't fail fast.

    # pylint: disable=bare-except,broad-except
    # noinspection PyBroadException
    try:
        # https://api.ipify.org # fails on VPN.
        ip = requests.get(ipify).text
        return ip
    except BaseException:  # noqa
        return ""


PUBLIC_IP = check_public_ip()


def load_config() -> configparser.SectionProxy:
    """
    Load config
    """
    config = configparser.ConfigParser()
    config.read(".config/.pynt")
    return config["DEFAULT"]


SECTION = load_config()
PROJECT_NAME = SECTION["PROJECT_NAME"]

SRC = SECTION["SRC"]
PROBLEMS_FOLDER = SECTION["PROBLEMS_FOLDER"]
REPORTS_FOLDER = SECTION["REPORTS_FOLDER"]
IS_SHELL_SCRIPT_LIKE = SECTION["IS_SHELL_SCRIPT_LIKE"]
COMPLEXITY_CUT_OFF = SECTION["COMPLEXITY_CUT_OFF"]

# pylint: disable=invalid-name
FuncType = Callable[..., Any]
# pylint: disable=invalid-name
F = TypeVar("F", bound=FuncType)


def initialize_folders() -> None:
    """
    Create folders that are likely to be needed
    """
    for folder in [PROBLEMS_FOLDER, REPORTS_FOLDER]:
        if not os.path.exists(folder):
            os.mkdir(folder)


initialize_folders()

VENV_SHELL = SECTION["VENV_SHELL"]

# pylint: disable=simplifiable-if-expression
# uh... need mechanism to show preference for no venv, poetry or pipenv.
# WANT_TO_USE_PIPENV = True if VENV_SHELL else False
PIPENV_ACTIVE = "PIPENV_ACTIVE" in os.environ and os.environ["PIPENV_ACTIVE"] == "1"
POETRY_ACTIVE = "POETRY_ACTIVE" in os.environ and os.environ["POETRY_ACTIVE"] == "1"

if PIPENV_ACTIVE or POETRY_ACTIVE:
    # activating each run is very, very slow.
    VENV_SHELL = ""

MINIMUM_TEST_COVERAGE = int(SECTION["MINIMUM_TEST_COVERAGE"])
SMALL_CODE_BASE_CUTOFF = int(SECTION["SMALL_CODE_BASE_CUTOFF"])
MAXIMUM_LINT = int(SECTION["MAXIMUM_LINT"])
MAXIMUM_MYPY = int(SECTION["MAXIMUM_MYPY"])
MAXIMUM_DEAD_CODE = int(SECTION["MAXIMUM_DEAD_CODE"])
MAXIMUM_MANIFEST_ERRORS = int(SECTION["MAXIMUM_MANIFEST_ERRORS"])

PYTHON = "python"
IS_DJANGO = False
IS_GITLAB = "GITLAB_CI" in os.environ
IS_WINDOWS = platform.system() == "Windows"
IS_ALPINE_DOCKER = os.path.exists("/etc/alpine-release")
IS_JENKINS = "FROM_JENKINS" in os.environ and os.environ["FROM_JENKINS"] == "TRUE"

CURRENT_HASH = None

VENDOR_LIBS = ":"

# so that formatting doesn't run after check done once
FORMATTING_CHECK_DONE = False


# Keep this ugly comment as a warning for the next person.
# This .py file is so long because pynt breaks ordinary imports, but
# doesn't break import from an pip installed module.
# pynt does something with paths that makes it hard to import as per usual.
# pylint: disable=wrong-import-position
# sys.path.append(os.path.join(os.path.dirname(__file__), "."))
# import build_utils
# from build_utils import (
#     check_is_aws,
#     skip_if_no_change,
#     execute_with_environment,
#     execute_get_text,
#     say_and_exit,
#     check_command_exists,
#     timed,
#     skip_if_this_file_does_not_change,
#     is_cmd_exe,
#     is_windows,
# )  # noqa: E402


def is_windows() -> bool:
    """Guess if windows"""
    platform_string = platform.system()
    return os.name == "nt" or platform_string == "Windows" or "_NT" in platform_string


def is_powershell() -> bool:
    """
    Check if parent process or other ancestor process is powershell
    """
    # ref https://stackoverflow.com/a/55598796/33264
    # Get the parent process name.

    try:
        process_name = psutil.Process(os.getppid()).name()
        grand_process_name = psutil.Process(os.getppid()).parent().name()
        # See if it is Windows PowerShell (powershell.exe) or PowerShell Core
        # (pwsh[.exe]):
        is_that_shell = bool(re.fullmatch("pwsh|pwsh.exe|powershell.exe", process_name))
        if not is_that_shell:
            is_that_shell = bool(
                re.fullmatch("pwsh|pwsh.exe|powershell.exe", grand_process_name)
            )
    except psutil.NoSuchProcess:
        print("Can't tell if this is powershell, assuming not.")
        is_that_shell = False
    return is_that_shell


def is_cmd_exe() -> bool:
    """
    Check if parent process or other ancestor process is cmd
    """
    # ref https://stackoverflow.com/a/55598796/33264
    # Get the parent process name.
    try:
        process_name = psutil.Process(os.getppid()).name()
        grand_process_name = psutil.Process(os.getppid()).parent().name()
        # pylint: disable=bare-except, broad-except
        try:
            great_grand_process_name = (
                psutil.Process(os.getppid()).parent().parent().name()
            )
        except:  # noqa: B001
            great_grand_process_name = "No great grandparent"

        print(process_name, grand_process_name, great_grand_process_name)
        is_that_shell = bool(re.fullmatch("cmd|cmd.exe", process_name))
        if not is_that_shell:
            is_that_shell = bool(re.fullmatch("cmd|cmd.exe", grand_process_name))
        if not is_that_shell:
            is_that_shell = bool(re.fullmatch("cmd|cmd.exe", great_grand_process_name))
    except psutil.NoSuchProcess:
        print("Can't tell if this is cmd.exe, assuming not.")
        is_that_shell = False
    return is_that_shell


def check_command_exists(
    command: str, throw_on_missing: bool = False, exit_on_missing: bool = True
) -> bool:
    """
    Check if exists by a variety of methods that vary by shell
    """
    if not os.path.exists(".config/.build_state"):
        os.mkdir(".config/.build_state")
    state_file = ".config/.build_state/exists_" + command + ".txt"
    if os.path.exists(state_file):
        return True
    venv_shell = [_ for _ in VENV_SHELL.split(" ") if _ != ""]

    # Build command & print. Must do here or the print gets redirected!
    # these commands lack a --version.
    if command in ["pyroma", "liccheck", "pipenv_to_requirements", "pyupgrade", "pyt"]:
        # will fail unless bash shell
        if is_powershell():
            cmd = venv_shell + ["powershell", "get-command", command]
            # print(cmd)
        else:
            cmd = venv_shell + ["which", command]
            # print(cmd)
    else:
        cmd = venv_shell + [command, "--version"]
        # print(cmd)

    # pylint: disable=broad-except
    try:
        with io.StringIO() as buf, io.StringIO() as buf2, redirect_stdout(
            buf
        ), redirect_stderr(buf2):
            # execute command built up above.
            _ = subprocess.check_output(cmd)
            output = buf.getvalue()
            output2 = buf2.getvalue()
            print(output, output2)
            if "not recognized" in output or "not recognized" in output2:
                print(f"Got error checking if {command} exists")
                if throw_on_missing:
                    raise TypeError("Can't find command")
                if exit_on_missing:
                    sys.exit(-1)
                return False
            with open(
                ".config/.build_state/exists_" + command + ".txt", "w+"
            ) as handle:
                handle.write("OK")
    except OSError as os_error:
        print(os_error)
        print(f"Got error checking if {command} exists")
        if throw_on_missing:
            raise
        if exit_on_missing:
            sys.exit(-1)
        return False
    except Exception as ex:
        print("Other error")
        print(ex)
        print(f"Got error checking if {command} exists")
        if throw_on_missing:
            raise
        if exit_on_missing:
            sys.exit(-1)
        return False
    return True


def check_is_aws() -> bool:
    """
    Look at domain name to see if this is an ec2 machine
    """
    name = socket.getfqdn()
    return "ip-" in name and ".ec2.internal" in name


# bash to find what has change recently
# find src/ -type f -print0 | xargs -0 stat -f "%m %N" | sort -rn | head -10 |
# cut -f2- -d" "
class BuildState:
    """
    Try not to re-do what doesn't need to be redone
    """

    def __init__(self, what: str, where: str) -> None:
        """
        Set initial state
        """
        self.what = what
        self.where = where
        if not os.path.exists(".config/.build_state"):
            os.makedirs(".config/.build_state")
        self.state_file_name = f".config/.build_state/last_change_{what}.txt"

    def oh_never_mind(self) -> None:
        """
        If a task fails, we don't care if it didn't change since last, re-run,
        """
        # noinspection PyBroadException
        # pylint: disable=bare-except
        try:
            os.remove(self.state_file_name)
        except:  # noqa: B001
            pass

    def has_source_code_tree_changed(self) -> bool:
        """
        If a task succeeds & is re-run and didn't change, we might not
        want to re-run it if it depends *only* on source code
        """
        # pylint: disable=global-statement
        global CURRENT_HASH
        directory = self.where

        # if CURRENT_HASH is None:
        # print("hashing " + directory)
        # print(os.listdir(directory))
        CURRENT_HASH = dirhash(
            directory,
            "md5",
            ignore_hidden=True,
            # changing these exclusions can cause dirhas to skip EVERYTHING
            # excluded_files=[".coverage", "lint.txt"],
            excluded_extensions=[".pyc"],
        )

        print("Searching " + self.state_file_name)
        if os.path.isfile(self.state_file_name):
            with open(self.state_file_name, "r+") as file:
                last_hash = file.read()
                if last_hash != CURRENT_HASH:
                    file.seek(0)
                    file.write(CURRENT_HASH)
                    file.truncate()
                    return True
                return False

        # no previous file, by definition not the same.
        with open(self.state_file_name, "w") as file:
            file.write(CURRENT_HASH)
            return True


def oh_never_mind(what: str) -> None:
    """
    If task fails, remove file that says it was recently run.
    Needs to be like this because tasks can change code (and change the hash)
    """
    state = BuildState(what, PROJECT_NAME)
    state.oh_never_mind()


def has_source_code_tree_changed(
    task_name: str, expect_file: Optional[str] = None
) -> bool:
    """
    Hash source code tree to know if it has changed

    Also check if an expected output file exists or not.
    """
    if expect_file:
        if os.path.isdir(expect_file) and not os.listdir(expect_file):
            os.path.dirname(expect_file)
            # output folder empty
            return True
        if not os.path.isfile(expect_file):
            # output file gone
            return True
    state = BuildState(task_name, os.path.join(SRC, PROJECT_NAME))
    return state.has_source_code_tree_changed()


def skip_if_no_change(name: str, expect_files: Optional[str] = None) -> F:
    """
    Don't run decorated task if nothing in the source has changed.
    """

    # https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def real_decorator(func: F) -> F:
        """Wrapper"""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            """Wrapper"""
            if not has_source_code_tree_changed(name, expect_files):
                print("Nothing changed, won't re-" + name)
                return lambda x: None
            try:
                return func(*args, **kwargs)
            except:  # noqa: B001
                oh_never_mind(name)
                raise

        return cast(F, wrapper)

    return cast(F, real_decorator)


def hash_it(path: str) -> str:
    """
    Hash a single file. Return constant if it doesn't exist.
    """
    if not os.path.exists(path):
        return "DOESNOTEXIST"
    with open(path, "rb") as file_handle:
        return hashlib.sha256(file_handle.read()).hexdigest()


def skip_if_this_file_does_not_change(name: str, file: str) -> F:
    """
    Skip decorated task if this referenced file didn't change. Useful
    if a task depends on a single file and not (potentially) any file in the source tree
    """

    def real_decorator(func: F) -> F:
        """Wrapper"""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            """Wrapper"""
            state_file = ".config/.build_state/file_hash_" + name + ".txt"
            previous_hash = "catdog"
            if os.path.exists(state_file):
                with open(state_file) as old_file:
                    previous_hash = old_file.read()

            new_hash = hash_it(file)
            if new_hash == previous_hash:
                print("Nothing changed, won't re-" + name)
                return lambda x: f"Skipping {name}, no change"
            if not os.path.exists(".config/.build_state"):
                os.mkdir(".config/.build_state")
            with open(state_file, "w+") as state:
                state.write(new_hash)
            try:

                return func(*args, **kwargs)
            except:  # noqa: B001
                # reset if step fails
                os.remove(state_file)
                raise

        return cast(F, wrapper)

    return cast(F, real_decorator)


def execute_with_environment(command: str, env: Dict[str, str]) -> Tuple[bytes, bytes]:
    """
    Yet another helper to execute a command
    """
    # Python 2 code! Python 3 uses context managers.
    command_text = command.strip().replace("  ", " ")
    command_parts = shlex.split(command_text)
    shell_process = subprocess.Popen(command_parts, env=env)
    value = shell_process.communicate()  # wait
    if shell_process.returncode != 0:
        print(f"Didn't get a zero return code, got : {shell_process.returncode}")
        sys.exit(-1)
    return value


def execute_get_text(
    command: List[str],
    ignore_error: bool = False,
    # shell: bool = True, # causes cross plat probs, security warnings, etc.
    env: Optional[Dict[str, str]] = None,
) -> str:
    """
    Execute shell command and return stdout txt
    """
    if env is None:
        env = {}

    completed = None
    try:
        completed = subprocess.run(
            command,
            check=not ignore_error,
            # shell=shell, # causes cross plat probs, security warnings, etc.
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


def say_and_exit(message: str, source: str) -> None:
    """
    Broken now. When it works, it was to audibly notify the developer that the build is
    done so that long builds wouldn't cause an attention problem
    """
    print(message, source)
    # if check_command_exists("say"):
    #     if not IS_GITLAB and not check_is_aws():
    #         # TODO: check a profile option or something.
    #         subprocess.call(["say", message])
    sys.exit(-1)


def secrets_ini_or_env(key: str) -> str:
    """
    Look up a secret using an ad hoc secrets.ini file.
    Superceded by dotenv
    """
    secret_config = configparser.ConfigParser()
    config_path = os.path.expanduser("~/.secrets/secrets.ini")
    secret_config.read(config_path)
    print(x for x in secret_config["DEFAULT"])
    secret_section = secret_config["DEFAULT"]
    try:
        value = secret_section[key]
        return value
    except KeyError:
        try:
            value = os.environ[key]
            return value
        except KeyError:
            print(f"Can't find {key} in {config_path} or in ENV")
            sys.exit(-1)


def timed() -> F:
    """This decorator prints the execution time for the decorated function."""

    def real_decorator(func: F) -> F:
        """Wrapper"""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            """Wrapper"""
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print("{} ran in {}s".format(func.__name__, round(end - start, 2)))
            return result

        return cast(F, wrapper)

    return cast(F, real_decorator)


def is_it_worse(task_name: str, current_rows: int, margin: int) -> bool:
    """
    Logic for dealing with a code base with very large amounts of lint.

    You will never fix it all, just don't make it worse.
    """
    if not os.path.exists(".config/.build_state"):
        os.makedirs(".config/.build_state")
    file_name = f".config/.build_state/last_count_{task_name}.txt"

    last_rows = sys.maxsize
    if os.path.isfile(file_name):
        with open(file_name, "r+") as file:
            last_rows = int(file.read())
            if last_rows != current_rows:
                file.seek(0)
                file.write(str(current_rows))
                file.truncate()

    return current_rows > (last_rows + margin)


# If node exists, we can run node build tools.
NODE_EXISTS = check_command_exists(
    "node", throw_on_missing=False, exit_on_missing=False
)


def clean_old_files() -> None:
    """
    Output files all moved to /problems/ or /reports/, clean up
    detritus left by old versions of build.py
    """
    for file in [
        "dead_code.txt",
        "lint.txt",
        "mypy_errors.txt",
        "line_counts.txt",
        "manifest_errors.txt",
        "detect-secrets-results.txt",
    ]:
        if os.path.exists(file):
            os.remove(file)


clean_old_files()


def prep_print_simple(command: str, no_project: bool = False) -> str:
    """
    Deal with simple command that only takes project name as arg
    """
    if no_project:
        command = f"{VENV_SHELL} {command}".strip().replace("  ", " ")
    else:
        command = f"{VENV_SHELL} {command} {PROJECT_NAME}".strip().replace("  ", " ")
    print(command)
    return command


@task()
@timed()
def check_python_version() -> None:
    """
    Possibly should look up min value in Pipenv or .pynt
    """
    print(sys.version_info)
    if sys.version_info[0] < 3:
        print("Must be using Python 3.7")
        sys.exit(-1)
    if sys.version_info[1] < 7:
        print("Must be using Python 3.7 or greater")
        sys.exit(-1)


@task(check_python_version)
@skip_if_no_change("compile_py")
@timed()
def compile_py() -> None:
    """
    Basic syntax check with compileall flag
    """
    do_compile_py()


def do_compile_py() -> str:
    """
    Catch only the worst syntax errors
    """
    with safe_cd(SRC):
        command_text = f"{PYTHON} -m compileall"
        command_text = prep_print_simple(command_text)
        command = shlex.split(command_text)
        result = execute_get_text(command, env=config_pythonpath())
        print(result)
        assert result
    return "compileall succeeded"


@task()
@timed()
def validate_project_name() -> None:
    """
    Verify that all projects/modules are explicitly declared
    """
    found = setuptools.find_packages()
    # Just care about root
    found = [name for name in found if "." not in name and name != "test"]
    problems = 0
    if not found:
        print("Found more than no modules at all, did you forget __init__.py?")
        problems += 1

    if len(found) > 1:
        print(f"Found more than one module, found {found}")
        problems += 1
    if PROJECT_NAME not in found:
        print(f"Can't find {PROJECT_NAME}, found {found}")
        problems += 1
    if problems > 0:
        sys.exit(-1)


@task()
@timed()
@skip_if_this_file_does_not_change("installs", file="Pipfile")
def pipenv_installs() -> None:
    """
    Catch up on installs, but only when Pipfile changes because
    pipenv is so slow
    """
    if PIPENV_ACTIVE:
        check_command_exists("pipenv")
        command_text = f"pipenv install --dev --skip-lock"
        print(command_text)
        command = shlex.split(command_text)
        execute(*command)
    elif POETRY_ACTIVE:
        check_command_exists("poetry")
        command_text = f"poetry install"
        print(command_text)
        command = shlex.split(command_text)
        execute(*command)
    else:
        print("VENV not previously activated, won't attempt to catch up on installs")
    # else:
    #     if os.path.exists("requirements.txt"):
    #         command_text = "pip install -r requirements.txt"
    #         print(command_text)
    #         command = shlex.split(command_text)
    #         execute(*command)
    #     else:
    #         print("no requirements.txt file yet, can't install dependencies")
    #
    #     if os.path.exists("requirements-dev.txt"):
    #         command_text = "pip install -r requirements-dev.txt"
    #         print(command_text)
    #         command = shlex.split(command_text)
    #         execute(*command)
    #     else:
    #         print("no requirements-dev.txt file yet, can't install dependencies")


@task()
@timed()
def gitchangelog() -> None:
    """
    Create a change log from git comments
    """
    # TODO: this app has lots of features for cleaning up comments
    command_name = "gitchangelog"
    check_command_exists(command_name)
    with safe_cd(SRC):
        command_text = f"{VENV_SHELL} {command_name}".strip().replace("  ", " ")
        print(command_text)
        command = shlex.split(command_text)
        with open("ChangeLog", "w+") as change_log:
            change_log.write(
                execute_get_text(command, env=config_pythonpath()).replace("\r", "")
            )


@task()
@timed()
def spell_check() -> None:
    """
    Check spelling using scspell (pip install scspell3k)
    """
    # tool can't recurse through files
    # tool returns a hard to parse format
    # tool has a really cumbersome way of adding values to dictionary
    walk_dir = PROJECT_NAME
    files_to_check = []
    print(walk_dir)
    for root, _, files in os.walk(walk_dir):
        if "pycache" in root:
            continue
        for file in files:
            print(root + "/" + file)
            if file.endswith(".py"):
                files_to_check.append(root + "/" + file)

    files_to_check_string = " ".join(files_to_check)
    command_text = (
        f"{VENV_SHELL} scspell --report-only "
        f"--override-dictionary=spelling_dictionary.txt "
        f"--use-builtin-base-dict {files_to_check_string}".strip().replace("  ", " ")
    )
    print(command_text)
    command = shlex.split(command_text)
    result = execute_get_text(command, ignore_error=True, env=config_pythonpath())
    with open(f"{PROBLEMS_FOLDER}/spelling.txt", "w+") as outfile:
        outfile.write(
            "\n".join(
                [
                    row
                    for row in result.replace("\r", "").split("\n")
                    if "dictionary" in row
                ]
            )
        )

    def read_file() -> None:
        with open("spelling.txt") as reading_file:
            reading_result = reading_file.read()
            print(
                "\n".join(
                    [row for row in reading_result.split("\n") if "dictionary" in row]
                )
            )

    read_file()


def dist_is_editable() -> bool:
    """Is distribution an editable install?"""
    for path_item in sys.path:
        egg_link = os.path.join(path_item, PROJECT_NAME + ".egg-link")
        if os.path.isfile(egg_link):
            return True
    return False


@task()
@skip_if_no_change("config_scripts")
@timed()
def register_scripts() -> None:
    """
    Without this console_scripts in the entrypoints section of setup.py aren't
    available
    :return:
    """
    check_command_exists("pip")

    # This doesn't work, it can't tell if "install -e ." has already run
    if dist_is_editable():
        print("console_scripts already registered")
        return
    # install in "editable" mode
    command_text = f"{VENV_SHELL} pip install -e ."
    print(command_text)
    command_text = command_text.strip().replace("  ", " ")
    command = shlex.split(command_text)
    execute(*command)


@task()
@skip_if_this_file_does_not_change("openapi_check", f"{PROJECT_NAME}/api.yaml")
@timed()
def openapi_check() -> None:
    """
    Does swagger/openapi file parse
    """
    if not os.path.exists(f"{PROJECT_NAME}/api.yaml"):
        print("No api.yaml file, assuming this is not a microservice")
        return

    command_text = (
        f"{VENV_SHELL} "
        f"openapi-spec-validator"
        f" {PROJECT_NAME}/api.yaml".strip().replace("  ", " ")
    )
    print(command_text)
    command = shlex.split(command_text)
    execute(*command)

    if IS_JENKINS or IS_GITLAB:
        print("Jenkins/Gitlab and apistar don't work together, skipping")
        return

    command_text = (
        f"{VENV_SHELL} apistar validate "
        f"--path {PROJECT_NAME}/api.yaml "
        f"--format openapi "
        f"--encoding yaml".strip().replace("  ", " ")
    )
    print(command_text)
    # subprocess.check_call(command.split(" "), shell=False)
    command = shlex.split(command_text)
    result = execute_get_text(command, ignore_error=True, env=config_pythonpath())
    if "OK" not in result and "2713" not in result and "✓" not in result:
        print(result)
        print("apistar didn't like this")
        sys.exit(-1)


@task()
@skip_if_no_change("count_lines_of_code")
@timed()
def count_lines_of_code() -> None:
    """
    Count lines of code to set build strictness
    """
    do_count_lines_of_code()


def total_loc() -> int:
    """
    Get Lines of Code for app
    """
    if not os.path.exists(".config/.build_state"):
        os.mkdir(".config/.build_state")
    # pylint: disable=bare-except
    try:
        with open(".config/.build_state/pygount_total_loc.txt") as file_handle:
            total_loc_value = file_handle.read()
    except:  # noqa: B001
        do_count_lines_of_code()
        with open(".config/.build_state/pygount_total_loc.txt") as file_handle:
            total_loc_value = file_handle.read()

    return int(total_loc_value)


def do_count_lines_of_code() -> None:
    """
    Scale failure cut offs based on Lines of Code
    """
    command_name = "pygount"
    check_command_exists(command_name)
    command_text = prep_print_simple(command_name)

    # keep out of src tree, causes extraneous change detections
    if not os.path.exists(f"{REPORTS_FOLDER}"):
        os.mkdir(f"{REPORTS_FOLDER}")
    output_file_name = f"{REPORTS_FOLDER}/line_counts.txt"
    command = shlex.split(command_text)
    with open(output_file_name, "w") as outfile:
        subprocess.call(command, stdout=outfile)

    with open(output_file_name) as file_handle:
        lines = sum(int(line.split("\t")[0]) for line in file_handle if line != "\n")

    total_loc_local = lines
    if not os.path.exists(".config/.build_state"):
        os.mkdir(".config/.build_state")
    with open(".config/.build_state/pygount_total_loc.txt", "w+") as state_file:
        state_file.write(str(total_loc_local))

    print(f"Lines of code: {total_loc_local}")
    if total_loc_local == 0:
        say_and_exit(
            "No code found to build or package. Maybe the PROJECT_NAME is wrong?",
            "lines of code",
        )


@task()
@skip_if_no_change("git_leaks")
@timed()
def git_leaks() -> None:
    """
    Depends on go!
    """
    run_gitleaks()


@task()
@skip_if_no_change("git_secrets")
@timed()
def git_secrets() -> None:
    """
    Run git secrets utility
    """
    # do_git_secrets()


def do_git_secrets() -> str:
    """
    Install git secrets if possible.
    """
    return
    if is_cmd_exe():
        print("git secrets is a bash script, only works in bash (or maybe PS")
        return "skipped git secrets, this is cmd.exe shell"
    if IS_ALPINE_DOCKER:
        return "Alpine docker, not sure how to install git secrets here."
    # not sure how to check for a git subcommand
    check_command_exists("git")

    if check_is_aws():
        # no easy way to install git secrets on ubuntu.
        return "This is AWS, not doing git-secrets"
    if IS_GITLAB:
        print("Nothing is edited on gitlab build server")
        return "This is gitlab, not doing git-secrets"
    try:
        # check to see if secrets even is a git command

        commands = ["git secrets --install", "git secrets --register-aws"]
        for command in commands:
            command_parts = shlex.split(command)
            command_process = subprocess.run(
                command_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            for stream in [command_process.stdout, command_process.stderr]:
                if stream:
                    for line in stream.decode().split("\n"):
                        print("*" + line)
    except subprocess.CalledProcessError as cpe:
        print(cpe)
        installed = False
        for stream in [cpe.stdout, cpe.stderr]:
            if stream:
                for line in stream.decode().split("\n"):
                    print("-" + line)
                    if "commit-msg already exists" in line:
                        print("git secrets installed.")
                        installed = True
                        break
        if not installed:
            raise
    command_text = "git secrets --scan -r ./".strip().replace("  ", " ")
    command_parts = shlex.split(command_text)
    execute(*command_parts)
    return "git-secrets succeeded"


@task()
@timed()
def reset() -> None:
    """
    Delete all .build_state & to force all steps to re-run next build
    """
    if os.path.exists(".config/.build_state"):
        shutil.rmtree(".config/.build_state")
    if not os.path.exists(".config/.build_state"):
        os.mkdir(".config/.build_state")


@task(pipenv_installs)
@skip_if_no_change("pyupgrade")
@timed()
def pyupgrade() -> str:
    """
    Reformat code to use py3 patterns when possible
    """
    command = "pyupgrade"
    check_command_exists(command)

    all_files = " ".join(
        f for f in glob.glob(f"{PROJECT_NAME}/**/*.py", recursive=True)
    )
    with safe_cd(SRC):
        command = (
            f"{VENV_SHELL} pyupgrade "
            f"--py37-plus "
            f"--exit-zero-even-if-changed {all_files}".strip().replace("  ", " ")
        )
        print(command)
        execute(*(command.split(" ")))
    return f"{command} succeeded"


@task()
@timed()
def isort() -> None:
    """Sort the imports to discover import order bugs and prevent import order bugs"""
    # This must run before black. black doesn't change import order but it wins
    # any arguments about formatting.
    # isort MUST be installed with pipx! It is not compatible with pylint in the same
    # venv. Maybe someday, but it just isn't worth the effort.
    with safe_cd(SRC):
        check_command_exists("isort")
        command = "isort --profile black"
        command = prep_print_simple(command)
        execute(*(command.split(" ")))
    return "isort succeeded"


@task(pipenv_installs, pyupgrade, compile_py, isort)
@skip_if_no_change("formatting")
@timed()
def formatting() -> None:
    """
    Format main project with black
    """
    do_formatting("")


@task()
@skip_if_no_change("format_tests")
@timed()
def format_tests() -> None:
    """
    Format unit tests with black
    """
    do_formatting("test")


@task(pipenv_installs, compile_py)
@timed()
def formatting_check() -> None:
    """
    Call with check parameter
    """
    do_formatting("--check")


def do_formatting(check: str) -> None:
    """
    Format with black - this will modify code if check is --check
    """
    # pylint: disable=global-statement
    global FORMATTING_CHECK_DONE
    if FORMATTING_CHECK_DONE:
        print("Formatting check says black will not reformat, so no need to repeat")
        return
    if sys.version_info < (3, 6):
        print("Black doesn't work on python 2")
        return
    check_command_exists("black")
    with safe_cd(SRC):
        command_text = f"{VENV_SHELL} black {PROJECT_NAME} {check}".strip().replace(
            "  ", " "
        )
        print(command_text)
        command = shlex.split(command_text)
        if check:
            _ = execute(*command)
            FORMATTING_CHECK_DONE = True
            return
        result = execute_get_text(command, env=config_pythonpath())
        assert result
        changed = []
        for line in result.split("\n"):
            if "reformatted " in line:
                file = line[len("reformatted ") :].strip()
                changed.append(file)
        # if not IS_GITLAB:
        #     for change in changed:
        #         if is_windows():
        #             change = change.replace("\\", "/")
        #         command_text = f"git add {change}"
        #         print(command_text)
        #         command = shlex.split(command_text)
        #         execute(*command)


@task()
@timed()
@skip_if_this_file_does_not_change("pyroma", "setup.py")
def pyroma() -> None:
    """
    Pyroma linter
    """
    # technically, this can depend on setup.py or setup.cfg...
    do_pyroma()


def do_pyroma() -> str:
    """
    Check package goodness (essentially lints setup.py)
    """
    command = "pyroma"
    check_command_exists(command)
    if os.path.exists("setup.py") or os.path.exists("setup.cfg"):
        with safe_cd(SRC):
            command = f"{VENV_SHELL} pyroma --directory --min=8 .".strip().replace(
                "  ", " "
            )
            print(command)
            execute(*(command.split(" ")))
    return "pyroma succeeded"


@task()
@skip_if_this_file_does_not_change("docker_lint", "Dockerfile")
@timed()
def docker_lint() -> None:
    """
    Lint the dockerfile
    """
    with open("Dockerfile") as my_input, open(
        f"{PROBLEMS_FOLDER}/docker_lint.txt", "w"
    ) as my_output:
        # ignore = ""  # "--ignore DL3003 --ignore DL3006"
        command = "docker run --rm -i hadolint/hadolint hadolint -".strip()
        _ = subprocess.run(command, stdin=my_input, stdout=my_output, check=True)


@task()
@skip_if_no_change("yamllint")
@timed()
def yaml_lint() -> str:
    """
    Check yaml files for problems
    """
    command = "yamllint"
    check_command_exists(command)
    with safe_cd(SRC):
        command = f"{VENV_SHELL} yamllint {PROJECT_NAME}".strip().replace("  ", " ")
        print(command)
        execute(*(command.split(" ")))
    return "yamllint succeeded"


@task(formatting, compile_py)
@skip_if_this_file_does_not_change("liccheck", "Pipfile")
@timed()
def liccheck() -> None:
    """
    Force an explicit decision about license of referenced packages
    """
    do_liccheck()


def do_liccheck() -> str:
    """
    Make an explicit decision about license of referenced packages
    """
    with safe_cd(SRC):
        check_command_exists("liccheck")
        if not os.path.exists(f".config/requirements.txt"):
            print("No requirements.txt file, assuming we have no external deps")
            return "Skipping, not requirements.txt"
        command = f"liccheck -r .config/requirements.txt -s .config/.license_rules -l paranoid"

        command = prep_print_simple(command, no_project=True)
        execute(*(command.split(" ")))
    return "liccheck succeeded"


@task(formatting, compile_py)
@skip_if_no_change("pyright")
@timed()
def pyright() -> None:
    """
    Pyright checks. NODEJS TOOOL!
    """
    do_pyright()


def do_pyright() -> str:
    """
    Execute pyright
    """
    with safe_cd(SRC):
        command = "pyright"
        if check_command_exists(command, throw_on_missing=False):
            # subprocess.check_call(("npm install -g pyright").split(" "), shell=True)
            print(
                "You must install pyright before doing pyright checks: "
                "npm install -g pyright"
            )
        command = prep_print_simple(command)
        command += "/**/*.py"
        execute(*(command.split(" ")))
    return "Pyright finished"


@task(formatting, compile_py)
@skip_if_no_change("flake8")
@timed()
def flake8() -> None:
    """
    Lint with flake8
    """
    do_flake8()


def do_flake8() -> str:
    """
    Flake8 Checks
    """
    # too strict if I include SO post source!
    return
    with safe_cd(SRC):
        command = "flake8 --config .config/.flake8"
        check_command_exists(command)
        command = prep_print_simple(command)
        execute(*(command.split(" ")))
    return "flake 8 succeeded"


@task(formatting, compile_py)
@skip_if_no_change("bandit")
@timed()
def bandit() -> None:
    """
    Security linting with bandit
    """
    do_bandit()


def do_bandit() -> str:
    """
    Security Checks
    """
    if IS_SHELL_SCRIPT_LIKE not in ["0", "1"]:
        print("IS_SHELL_SCRIPT_LIKE, in .pynt config should be 0 or 1")
    if IS_SHELL_SCRIPT_LIKE == "1":
        return (
            "Skipping bandit, this code is shell script-like so it has security"
            "issues on purpose."
        )

    with safe_cd(SRC):
        command = "bandit"
        check_command_exists(command)
        command = "bandit -r"
        command = prep_print_simple(command)
        execute(*(command.split(" ")))
    return "bandit succeeded"


@task(formatting, compile_py)
@skip_if_no_change("python_taint")
@timed()
def python_taint() -> None:
    """
    Security linting with pyt
    """
    do_python_taint()


def do_python_taint() -> str:
    """
    Security Checks
    """
    # this broken again?!
    return ""
    with safe_cd(SRC):
        command = "pyt"
        check_command_exists(command)
        command = "pyt -r"
        command = prep_print_simple(command)
        execute(*(command.split(" ")))


@task(flake8)
@skip_if_no_change("mccabe")
@timed()
def mccabe() -> None:
    """
    Complexity checking/reports with mccabe
    """
    do_mccabe()


def do_mccabe() -> str:
    """
    Complexity Checker
    """
    return  # this runs all flake8 not just mccabe
    with safe_cd(SRC):
        check_command_exists("flake8")  # yes, flake8, this is a plug in.
        # mccabe doesn't have a direct way to run it
        command_text = f"flake8 --max-complexity {COMPLEXITY_CUT_OFF}"
        command_text = prep_print_simple(command_text)
        command = shlex.split(command_text)
        execute(*command)
    return "mccabe succeeded"


@task(formatting, compile_py)
@skip_if_no_change("dodgy")
@timed()
def dodgy_check() -> None:
    """
    Linting with dodgy
    """
    do_dodgy()


def do_dodgy() -> str:
    """
    Checks for AWS keys, diffs, pem keys
    """
    # Not using the shell command version because it mysteriously failed
    # and this seems to work fine.
    warnings = dodgy_runner.run_checks(os.getcwd())
    if warnings:
        print("Dodgy found problems")
        for message in warnings:
            print(message)
        sys.exit(-1)
    return "dodgy succeeded"


@task()
@skip_if_no_change("detect_secrets")
@timed()
def detect_secrets() -> None:
    """
    Look for secrets using detect-secrets
    """
    return
    # pylint: disable=unreachable
    do_detect_secrets()


def do_detect_secrets() -> str:
    """
    Call detect-secrets tool

    I think this is the problem:

    # Code expects to stream output to file and then expects
    # interactive person, so code hangs. But also hangs in git-bash
    detect-secrets scan test_data/config.env > foo.txt
    detect-secrets audit foo.txt
    """
    return "Disabled, hangs when executed from python or gitbash"
    # pylint: disable=unreachable
    check_command_exists("detect-secrets")
    errors_file = f"{PROBLEMS_FOLDER}/detect-secrets-results.txt"
    command_text = (
        f"{VENV_SHELL} detect-secrets scan "
        f"--base64-limit 4 "
        # f"--exclude-files .idea|.min.js|.html|.xsd|"
        # f"lock.json|.scss|Pipfile.lock|.secrets.baseline|"
        # f"{PROBLEMS_FOLDER}/lint.txt|{errors_file}".strip().replace("  ", " ")
    )
    print(command_text)
    command = shlex.split(command_text)

    with open(errors_file, "w") as outfile:
        env = config_pythonpath()
        output = execute_get_text(command, ignore_error=False, env=env)
        outfile.write(output)
        # subprocess.call(command, stdout=outfile, env=env)

    with open(errors_file, "w+") as file_handle:
        text = file_handle.read()
        if not text:
            print("Failed to check for secrets")
            sys.exit(-1)
        file_handle.write(text)

    try:
        with open(errors_file) as json_file:
            data = json.load(json_file)

        if data["results"]:
            for result in data["results"]:
                print(result)
            say_and_exit(
                "detect-secrets has discovered high entropy strings, "
                "possibly passwords?",
                "detect-secrets",
            )
    except json.JSONDecodeError:
        pass
    return "Detect secrets completed."


@task(formatting_check)
@skip_if_no_change("precommit")
@timed()
def precommit() -> None:
    """
    Build time execution of pre-commit checks. Modifies code so run before linter.
    """
    if IS_GITLAB:
        print("Not running precommit")
        return

    check_command_exists("pre-commit")
    with safe_cd(SRC):
        command_text = f"{VENV_SHELL} pre-commit install".strip().replace("  ", " ")
        print(command_text)
        command = shlex.split(command_text)
        execute(*command)

        command_text = f"{VENV_SHELL} pre-commit run --all-files".strip().replace(
            "  ", " "
        )
        print(command_text)
        command = shlex.split(command_text)
        result = execute_get_text(command, ignore_error=True, env=config_pythonpath())
        assert result
        changed = []
        for line in result.split("\n"):
            if "changed " in line:
                file = line[len("reformatted ") :].strip()
                changed.append(file)
        if "FAILED" in result:
            print(result)
            print("Failed")
            sys.exit(-1)

        if not IS_GITLAB:
            for change in changed:
                command_text = f"git add {change}"
                print(command_text)
                # this breaks on windows!
                # command = shlex.split(command_text)
                execute(*command_text.split())


@task(compile_py, formatting, count_lines_of_code, openapi_check)
@skip_if_no_change("lint", expect_files=f"{PROBLEMS_FOLDER}/lint.txt")
@timed()
def lint() -> None:
    """
    Lint with pylint
    """
    do_lint(PROJECT_NAME)


@task(format_tests)
@skip_if_no_change("lint_tests", expect_files=f"{PROBLEMS_FOLDER}/lint_test.txt")
@timed()
def lint_tests() -> None:
    """
    Lint only the tests by a different rule set
    """
    do_lint("test")


def do_lint(folder_name: str) -> str:
    """
    Execute pylint
    """
    # pylint: disable=too-many-locals
    check_command_exists("pylint")
    if folder_name == PROJECT_NAME:
        pylintrc = ".config/.pylintrc"
        lint_output_file_name = f"{PROBLEMS_FOLDER}/lint.txt"
    else:
        pylintrc = f".config/.pylintrc_{folder_name}"
        lint_output_file_name = f"{PROBLEMS_FOLDER}/lint_{folder_name}.txt"

    with safe_cd(SRC):
        if os.path.isfile(lint_output_file_name):
            os.remove(lint_output_file_name)

        if IS_DJANGO:
            django_bits = "--load-plugins pylint_django "
        else:
            django_bits = ""

        # pylint: disable=pointless-string-statement
        command_text = (
            f"{VENV_SHELL} pylint {django_bits} " f"--rcfile={pylintrc} {folder_name} "
        )

        command_text += " "
        "--msg-template={path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
        "".strip().replace("  ", " ")

        print(command_text)
        command = shlex.split(command_text)

        with open(lint_output_file_name, "w") as outfile:
            env = config_pythonpath()
            subprocess.call(command, stdout=outfile, env=env)

        with open(lint_output_file_name) as file_handle:
            full_text = file_handle.read()
        lint_did_indeed_run = "Your code has been rated at" in full_text

        with open(lint_output_file_name) as file_handle:
            fatal_errors = sum(
                1
                for line in file_handle
                if "no-member" in line
                or "no-name-in-module" in line
                or "import-error" in line
                or ": E" in line
                or ": F" in line
            )

        if fatal_errors > 0:
            with open(lint_output_file_name) as file_handle:
                for line in file_handle:
                    if (
                        "no-member" in line
                        or "no-name-in-module" in line
                        or "import-error" in line
                        or ": E" in line
                        or ": F" in line
                    ):
                        print(line)

            message = f"Fatal lint errors : {fatal_errors}"
            if IS_GITLAB:
                with open(lint_output_file_name) as error_file:
                    print(error_file.read())
            say_and_exit(message, "lint")
            return message
        with open(lint_output_file_name) as lint_file_handle:
            for line in [
                line
                for line in lint_file_handle
                if not (
                    "*************" in line
                    or "---------------------" in line
                    or "Your code has been rated at" in line
                    or line == "\n"
                )
            ]:
                print(line)

        if total_loc() > SMALL_CODE_BASE_CUTOFF:
            cutoff = MAXIMUM_LINT
        else:
            cutoff = 0
        with open(lint_output_file_name) as lint_file_handle:
            num_lines = sum(
                1
                for line in lint_file_handle
                if not (
                    "*************" in line
                    or "---------------------" in line
                    or "Your code has been rated at" in line
                    or line == "\n"
                )
            )
    if num_lines > cutoff:
        print(f"Too many lines of lint : {num_lines}, max {cutoff}")
        sys.exit(-1)
    with open(lint_output_file_name) as lint_file_handle:
        num_lines_all_output = sum(1 for _ in lint_file_handle)
    if (
        not lint_did_indeed_run
        and num_lines_all_output == 0
        and os.path.isfile(lint_output_file_name)
    ):
        # should always have at least 'found 0 errors' in output

        # force lint to re-run, because empty file will be missing
        os.remove(lint_output_file_name)
        print("No lint messages at all, did pylint fail to run or is it installed?")
        sys.exit(-1)

    return "pylint succeeded"


@task()
@timed()
def tox() -> str:
    """
    See if everything works with python 3.8 and upcoming libraries
    """
    # If tox fails the build with 3.8 or some future library, that means
    # we can't migrate to 3.8 yet, or that we should stay with currently pinned
    # libraries. We should fail the overall build.
    #
    # Because we control our python version we don't have to support cross ver
    # compatibility, i.e. we are not supporting 2.7 & 3.x!
    command_name = "tox"
    check_command_exists(command_name)
    with safe_cd(SRC):
        command_text = f"{VENV_SHELL} {command_name}".strip().replace("  ", " ")
        print(command_text)
        command = shlex.split(command_text)
        execute(*command)
    return "tox succeeded"


# commenting out because of deteriorating support for nose library
# @task(lint, lint_tests)
# @timed()
# def nose_tests() -> None:
#     """
#     Nose tests
#     """
#
#     check_command_exists("nosetests")
#
#     if IS_DJANGO:
#         command = f"{PYTHON} manage.py test -v 2"
#         # We'd expect this to be MAC or a build server.
#         my_env = config_pythonpath()
#         execute_with_environment(command, env=my_env)
#     else:
#         my_env = config_pythonpath()
#         command_text = (
#             f"nosetests --where test --exe --with-coverage --cover-erase "
#             f"--with-xunit --cover-package={PROJECT_NAME} "
#             f"--cover-xml-file=coverage.xml "
#             f"--cover-xml --cover-min-percentage={MINIMUM_TEST_COVERAGE}"
#         )
#         command_text = f"{PIPENV} {command_text}".strip().replace("  ", " ")
#         print(command_text)
#         execute_with_environment(command_text, env=my_env)


def config_pythonpath() -> Dict[str, str]:
    """
    Add to PYTHONPATH
    """
    my_env = {
        "PYTHONIOENCODING": "utf-8",
        "LC_ALL": "en_US.UTF-8",
        "LANG": "en_US.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "",
    }
    for key, value in os.environ.items():
        my_env[key] = value
    my_env["PYTHONPATH"] = my_env.get("PYTHONPATH", "")  # + VENDOR_LIBS
    return my_env


@task()
@skip_if_no_change("pytest", expect_files=f"{PROBLEMS_FOLDER}/pytest.txt")
@timed()
def pytest() -> None:
    """
    Pytest and coverage, which replaces nose tests
    """
    check_command_exists("pytest")

    #  Somedays VPN just isn't there.

    test_folder = "test"
    minimum_coverage = MINIMUM_TEST_COVERAGE

    my_env = config_pythonpath()
    with safe_cd(SRC):
        command = (
            f"{VENV_SHELL} pytest {test_folder} -v "
            f"--junitxml={REPORTS_FOLDER}/sonar-unit-test-results.xml "
            "--cov-report xml "
            f"--cov={PROJECT_NAME} "
            f"--cov-fail-under {minimum_coverage}".strip().replace("  ", " ")
            + " --quiet"  # 15000 pages of call stack don't help anyone
        )
        # when it works, it is FAST. when it doesn't, we get lots of timeouts.
        # if not IS_GITLAB:
        #     command += f" -n {multiprocessing.cpu_count()} "
        if not IS_GITLAB:
            command += " -n 2 "

        print(command)
        execute_with_environment(command, my_env)
        print("Tests will not be re-run until code changes. Run pynt reset to force.")


@task()
@skip_if_no_change(
    "coverage_report", expect_files=f"{PROBLEMS_FOLDER}/coverage_report.txt"
)
@timed()
def coverage_report() -> None:
    """
    Just the coverage report
    """
    check_command_exists("pytest")

    my_env = config_pythonpath()
    with safe_cd(SRC):
        # generate report separate from cov-fail-under step.
        # py.test incorrectly reports 0.00 coverage,
        # but only when reports are generated.

        # Coverage report is (sometimes) broken. Need alternative to py.test?
        # This is consuming too much time to figure out why it
        # collects no tests & then fails on code 5

        test_folder = "test"

        command = (
            f"{VENV_SHELL} pytest {test_folder} -v "
            f"--cov-report html:coverage "
            f"--cov={PROJECT_NAME}".strip().replace("  ", " ")
        )
        if not IS_GITLAB:
            command += f" -n {multiprocessing.cpu_count()} "
        print(command)
        execute_with_environment(command, my_env)
        print("Coverage will not rerun until code changes. Run `pynt reset` to force")


@task()
@skip_if_no_change("docs")
@timed()
def docs() -> None:
    """
    Generate Sphynx documentation
    """
    do_docs()


def do_docs() -> str:
    """
    Call as normal function
    """
    check_command_exists("make")

    with safe_cd(SRC):
        with safe_cd("docs"):
            my_env = config_pythonpath()
            command = f"{VENV_SHELL} make html".strip().replace("  ", " ")
            print(command)
            execute_with_environment(command, env=my_env)
    return "Docs generated"


@task()
@timed()
@skip_if_this_file_does_not_change("pip_check", "Pipfile")
def pip_check() -> None:
    """
    pip check the packages
    """
    do_pip_check()


def do_pip_check() -> str:
    """
    Call as normal function
    """
    execute("pip", "check")
    environment = config_pythonpath()
    environment["PIPENV_PYUP_API_KEY"] = ""
    if PIPENV_ACTIVE:
        # ignore 38414 until aws fixes awscli
        execute_with_environment("pipenv check --ignore 38414", environment)
    return "Pip(env) check run"


@task()
@timed()
@skip_if_this_file_does_not_change("safety", "Pipfile")
def safety() -> None:
    """
    Run safety against pinned requirements
    """
    do_safety()


def do_safety() -> str:
    """
    Check free database for vulnerabilities in pinned libraries.
    """
    requirements_file_name = f".config/requirements_for_safety.txt"
    with open(requirements_file_name, "w+") as out:
        subprocess.run(["pip", "freeze"], stdout=out, stderr=out, check=True)
    check_command_exists("safety")
    # ignore 38414 until aws fixes awscli
    execute("safety", "check", "--ignore", "38414", "--file", requirements_file_name)
    return "Package safety checked"


@task()  # this depends on coverage! blows up if xml file doesn't match source
@skip_if_no_change("sonar", expect_files="sonar.json")
@timed()
def sonar() -> None:
    """
    Lint using remote sonar service
    """
    do_sonar()


def do_sonar() -> str:
    """
    Upload code to sonar for review
    """
    sonar_key = os.environ["SONAR_KEY"]
    if is_windows():
        command_name = "sonar-scanner.bat"
    else:
        command_name = "sonar-scanner"
    command = (
        f"{VENV_SHELL} {command_name} "
        f"-Dsonar.login={sonar_key} "
        f"-Dproject.settings="
        f"sonar-project.properties".strip().replace("  ", " ").split(" ")
    )
    print(command)
    execute(*command)
    url = f"https://?" f"componentKeys=public_record_{PROJECT_NAME}&resolved=false"

    session = requests.Session()
    session.auth = (sonar_key, "")

    response = session.get(url)

    errors_file = "sonar.json"
    with open(errors_file, "w+") as file_handle:
        print(response.text)
        text = response.text
        if not text:
            print("Failed to check for sonar")
            sys.exit(-1)
        file_handle.write(text)

    try:
        with open(errors_file) as f:
            data = json.load(f)

        if data["issues"]:
            for result in data["issues"]:
                print(
                    "{} : {} line {}-{}".format(
                        result["component"],
                        result["message"],
                        result["textRange"]["startLine"],
                        result["textRange"]["endLine"],
                    )
                )
            say_and_exit("sonar has issues with this code", "sonar")
    except json.JSONDecodeError:
        pass
    return "Sonar done"


@task(count_lines_of_code)
@skip_if_no_change("mypy", expect_files=f"{PROBLEMS_FOLDER}/mypy_errors.txt")
@timed()
def mypy() -> None:
    """
    Check types using mypy
    """
    do_mypy()


def do_mypy() -> str:
    """
    Are types ok?
    """
    check_command_exists("mypy")
    if sys.version_info < (3, 4):
        print("Mypy doesn't work on python < 3.4")
        return "command is missing"
    if IS_GITLAB:
        command = (
            f"{PYTHON} -m mypy {PROJECT_NAME} "
            f"--ignore-missing-imports "
            f"--strict".strip().replace("  ", " ")
        )
    else:
        command = (
            f"{VENV_SHELL} mypy {PROJECT_NAME} "
            f"--ignore-missing-imports "
            f"--strict".strip().replace("  ", " ")
        )
    print(command)
    bash_process = subprocess.Popen(
        command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, _ = bash_process.communicate()  # wait
    mypy_file = f"{PROBLEMS_FOLDER}/mypy_errors.txt"

    skips = [
        "tests.py",
        "/test_",
        "/tests_",
        # No clear way to type a decorator
        "Untyped decorator",
        "<nothing> not callable",
        'Returning Any from function declared to return "Callable[..., Any]"',
        'Missing type parameters for generic type "Callable"',
    ]

    def contains_a_skip(line_value: str) -> bool:
        """
        Should this line be skipped
        """
        # skips is a closure
        for skip in skips:
            if skip in line_value or line_value.startswith(skip):
                return True
        return False

    actually_bad_lines: List[str] = []
    total_lines = 0
    with open(mypy_file, "w+") as lint_file:
        lines = out.decode().split("\n")
        for line in lines:
            total_lines += 1
            if contains_a_skip(line):
                continue
            if not line.startswith(PROJECT_NAME):
                continue
            actually_bad_lines.append(line)
            lint_file.writelines([line])

    num_lines = len(actually_bad_lines)
    if total_loc() > SMALL_CODE_BASE_CUTOFF:
        max_lines = MAXIMUM_MYPY
    else:
        max_lines = 2  # off by 1 right now

    if num_lines > max_lines:
        for line in actually_bad_lines:
            print(line)
        print(f"Too many lines of mypy : {num_lines}, max {max_lines}")
        sys.exit(-1)

    if num_lines == 0 and total_lines == 0:
        # should always have at least 'found 0 errors' in output
        print("No mypy warnings at all, did mypy fail to run or is it installed?")
        sys.exit(-1)
    return "mypy succeeded"


@task()
@timed()
@skip_if_this_file_does_not_change("pin_dependencies", "Pipfile")
def pin_dependencies() -> None:
    """
    Create requirement*.txt
    """
    do_pin_dependencies()


def do_pin_dependencies() -> None:
    """
    Create requirement*.txt
    """
    check_command_exists("pipenv_to_requirements")

    with safe_cd(SRC):
        execute(
            *(
                f"{VENV_SHELL} pipenv_to_requirements --dev-output .config/requirements-dev.txt --output .config/requirements.txt".strip().split(
                    " "
                )
            )
        )
    if not os.path.exists(".config/requirements.txt"):
        print(
            "Warning: no requirments.txt found, assuming it is because there are"
            "no external dependencies yet"
        )
    else:
        with open(f".config/requirements.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if line.find("-e .") == -1:
                    file.write(line)
            file.truncate()

    with open(f".config/requirements-dev.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.find("-e .") == -1:
                file.write(line)
        file.truncate()


@task()
@skip_if_no_change("vulture", expect_files=f"{PROBLEMS_FOLDER}/dead_code.txt")
@timed()
def dead_code() -> None:
    """
    Find dead code using vulture
    """
    do_dead_code()


def do_dead_code() -> str:
    """
    This also finds code you are working on today!
    """

    check_command_exists("vulture")
    with safe_cd(SRC):
        # TODO: check if whitelist.py exists?
        command_text = (
            f"{VENV_SHELL} vulture {PROJECT_NAME} "
            f""
            f"whitelist.py".strip().replace("  ", " ")
        )
        print(command_text)
        command = shlex.split(command_text)

        output_file_name = f"{PROBLEMS_FOLDER}/dead_code.txt"
        with open(output_file_name, "w") as outfile:
            env = config_pythonpath()
            subprocess.call(command, stdout=outfile, env=env)

        if total_loc() > SMALL_CODE_BASE_CUTOFF:
            cutoff = MAXIMUM_DEAD_CODE
        else:
            cutoff = 0

        with open(output_file_name) as file_handle:
            num_lines = sum(1 for line in file_handle if line)
        if num_lines > cutoff:
            print(f"Too many lines of dead code : {num_lines}, max {cutoff}")
            sys.exit(-1)
    return "dead-code (vulture) succeeded"


def call_check_manifest_command(output_file_name: str, env: Dict[str, str]) -> None:
    """
    To allow for checking in multiple passes
    """
    return
    check_command_exists("check-manifest")

    command_text = f"{VENV_SHELL} check-manifest".strip().replace("  ", " ")

    with open(output_file_name, "w") as outfile:
        print(command_text)
        command = shlex.split(command_text)
        subprocess.call(command, stdout=outfile, env=env)


@task(count_lines_of_code)
@skip_if_no_change("check_manifest", f"{PROBLEMS_FOLDER}/manifest_errors.txt")
@timed()
def check_manifest() -> None:
    """
    Find files missing from MANIFEST.in
    """
    do_check_manifest()


def do_check_manifest() -> str:
    """
    Require all files to be explicity included/excluded from package
    """
    return
    env = config_pythonpath()
    output_file_name = f"{PROBLEMS_FOLDER}/manifest_errors.txt"
    call_check_manifest_command(output_file_name, env)

    with open(output_file_name) as outfile_reader:
        text = outfile_reader.read()

        print(text)
        if not os.path.isfile("MANIFEST.in") and "no MANIFEST.in found" in text:
            command_text = f"{VENV_SHELL} check-manifest -c".strip().replace("  ", " ")
            command = shlex.split(command_text)
            subprocess.call(command, env=env)
            # print("Had to create MANIFEST.in, please review and redo")
            call_check_manifest_command(output_file_name, env)

    if total_loc() > SMALL_CODE_BASE_CUTOFF:
        cutoff = 0
    else:
        cutoff = MAXIMUM_MANIFEST_ERRORS

    with open(output_file_name) as file_handle:
        num_lines = sum(
            1
            for line in file_handle
            if line
            and line.strip() != ""
            and "lists of files in version control and sdist match" not in line
        )
    if num_lines > cutoff:
        print(f"Too many lines of manifest problems : {num_lines}, max {cutoff}")
        sys.exit(-1)
    return "manifest check succeeded"


@task()
@timed()
def jiggle_version() -> None:
    """
    Increase build number of version, but only if this is the master branch.
    """
    # rorepo is a Repo instance pointing to the git-python repository.
    # For all you know, the first argument to Repo is a path to the repository
    # you want to work with
    if IS_GITLAB or IS_JENKINS:
        # never update version on build server
        return
    repo = Repo(".")
    if str(repo.active_branch) == "main":
        check_command_exists("jiggle_version")
        command = f"jiggle_version here --module={PROJECT_NAME}"
        parts = shlex.split(command)
        execute(*parts)
    else:
        print("Not main branch, not incrementing version")


@task(
    formatting,  # changes source
    # TODO: switch to parallel
    mypy,
    detect_secrets,
    git_secrets,
    dead_code,
    compile_py,
    lint,
    flake8,
    dodgy_check,
    bandit,
    python_taint,
    mccabe,
    pin_dependencies,
    jiggle_version,
    check_manifest,
    # tests as slow as tests are.
    pytest,
    # nose
    # package related
    liccheck,
    pyroma,
    pip_check,
    safety,
    precommit,  # I hope this doesn't change source anymore
)  # docs ... later
@skip_if_no_change("package")
@timed()
def package() -> None:
    """
    package, but don't upload
    """
    do_package()


@task()
@timed()
@skip_if_no_change("parallel_checks")
def parallel_checks() -> None:
    """
    Do all the checks that don't change code and can run in parallel.
    """
    chores = [
        do_mypy,
        do_detect_secrets,
        do_git_secrets,
        do_dead_code,
        do_compile_py,
        do_lint,
        do_flake8,
        do_dodgy,
        do_bandit,
        do_python_taint,
        do_mccabe,
        do_check_manifest,
        do_liccheck,
    ]
    if IS_GITLAB:
        # other tasks assume there will be a LOC file by now.
        do_count_lines_of_code()
        for chore in chores:
            print(chore())
        return

    # can't do pyroma because that needs a package, which might not exist yet.

    pool = ProcessPool(12)  # max_workers=len(chores))  # cpu_count())
    # log_to_stderr(logging.DEBUG)
    tasks = []
    for chore in chores:
        tasks.append(pool.schedule(chore, args=()))

    print("close & join")
    pool.close()
    pool.join()

    for current_task in tasks:
        # pylint: disable=broad-except
        try:
            result = current_task.result()
            exception = current_task.exception()
            if exception:
                print(current_task.exception())
            print(result)
            if "Abnormal" in str(result):
                print("One or more parallel tasks failed.")
                sys.exit(-1)
        except Exception as ex:
            print(ex)
            sys.exit(-1)


@task(
    mypy,  #
    detect_secrets,
    git_secrets,
    dead_code,
    compile_py,
    lint,
    flake8,
    dodgy_check,
    bandit,
    python_taint,
    mccabe,
    check_manifest,
    liccheck,  #
)  # docs ... later
@timed()
def slow() -> None:
    """
    Same tasks as parallel checks but in serial. For perf comparisons
    """


@task(
    formatting_check,  # changes source
    parallel_checks,
    # package related checks
    # pyroma, # depends on dist folder existing!
    # pip_check, # depends on dist folder existing!
    jiggle_version,  # changes source
    precommit,  # changes source
)  # docs ... later
@timed()
def fast_package() -> None:
    """
    Run most tasks in parallel
    """
    do_package()


@task()
@timed()
def just_package() -> None:
    """Package, but do no checks or tests at all"""
    print("WARNING: This skips all quality checks.")
    do_package()


def do_package() -> None:
    """
    don't do anything that is potentially really slow or that modifies files.
    """
    check_command_exists("twine")

    with safe_cd(SRC):
        for folder in ["build", "dist", PROJECT_NAME + ".egg-info"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                try:
                    original_umask = os.umask(0)
                    try:
                        os.makedirs(folder, 0o770)
                    except PermissionError:
                        execute("cmd", "mkdir", folder)
                finally:
                    os.umask(original_umask)

    with safe_cd(SRC):
        # command = f"{PYTHON} setup.py sdist --formats=gztar,zip"
        # bdist_wheel, setuptools, MANIFEST.in
        # and data_files is one clusterf*k of brokeness.
        command_text = f"{PYTHON} poetry build"
        command_text = prep_print_simple(command_text, no_project=True)
        command = shlex.split(command_text)
        result = execute_get_text(command, env=config_pythonpath()).replace("\r", "")

        error_count = 0
        for row in result.split("\n"):
            check_row = str(row).lower()
            if check_row.startswith("adding") or check_row.startswith("copying"):
                # adding a file named error/warning isn't a problem
                continue
            if "no previously-included files found matching" in check_row:
                # excluding a file that already doesn't exist is wonderful!
                # why this is a warning boggles the mind.
                continue
            # sometimes to avoid pyc getting out of sync with .py, on
            # dev workstations you PYTHONDONTWRITEBYTECODE=1 which just disables
            # pyc altogether. Why wheel cares, I don't know.
            has_error = any(
                value in check_row
                for value in ["Errno", "Error", "failed", "error", "warning"]
            )
            if has_error and "byte-compiling is disabled" not in check_row:
                print(row)
                error_count += 1
        if error_count > 0:
            sys.exit(-1)

        # pylint: disable=broad-except
        try:
            # Twine check must run after package creation. Supersedes setup.py check
            with safe_cd(SRC):
                command_text = f"{VENV_SHELL} twine check dist/*".strip().replace(
                    "  ", " "
                )
                print(command_text)
                command = shlex.split(command_text)
                execute(*command)
        except Exception as ex:
            print(ex)
            command_text = (
                f"{VENV_SHELL} setup.py "
                f"sdist "
                f"--formats=gztar,zip".strip().replace("  ", " ")
            )
            command = shlex.split(command_text)
            execute(*command)

            def list_files(startpath: str) -> None:
                """
                List all files, handy for remote build servers
                """
                for root, _, files in os.walk(startpath):
                    level = root.replace(startpath, "").count(os.sep)
                    indent = " " * 4 * (level)
                    print("{}{}/".format(indent, os.path.basename(root)))
                    subindent = " " * 4 * (level + 1)
                    for f in files:
                        print(f"{subindent}{f}")

            print("skipping twine check until I figure out what is up")
            list_files(startpath=".")


@task()
@timed()
def check_package() -> None:
    """
    Run twine check
    """
    check_command_exists("twine")
    with safe_cd(SRC):
        execute(*(f"{VENV_SHELL} twine check dist/*".strip().split(" ")))


@task()
@timed()
def upload_package() -> None:
    """
    Send to private package repo
    """
    # devpi use  http://localhost:3141
    # login with root...
    # devpi login root --password=
    # get indexes
    # devpi use -l
    # make an index
    # devpi index -c dev bases=root/pypi
    # devpi use root/dev

    # Must register (may go away with newer version of devpi), must be 1 file!
    # twine register --config-file .pypirc -r devpi-root -u root
    # -p PASSWORD dist/-0.1.0.zip
    # can be all files!
    # twine upload --config-file .pypirc -r devpi-root -u root -p PASSWORD dist/*

    # which is installable using...
    #  pip install search-service --index-url=http://localhost:3141/root/dev/

    check_command_exists("devpi")
    password = os.environ["DEVPI_PASSWORD"]
    any_zip = [file for file in os.listdir("dist") if file.endswith(".zip")][0]
    register_command = (
        f"twine register --config-file .pypirc -r devpi-root -u root"
        f" -p {password} dist/{any_zip}"
    )
    upload_command = (
        f"twine upload --config-file .pypirc -r devpi-root "
        f"-u root -p {password} dist/*"
    )
    with safe_cd(SRC):
        execute(*(register_command.strip().split(" ")))
        execute(*(upload_command.strip().split(" ")))


def run_gitleaks() -> None:
    """
    Run the gitleaks command.

    Depends on go!
    """
    #  git remote get-url --all origin
    # So far nothing works... as if current repo is corrupt
    cwd = os.getcwd()
    command_text = "gitleaks --repo-path={} --report=/tmp/{}.csv".format(
        cwd, PROJECT_NAME
    ).strip()
    print(command_text)
    command = shlex.split(command_text)
    _ = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            **os.environ,
            "GOPATH": os.path.expandvars("$HOME/gocode"),
            "PATH": os.path.expandvars("$PATH/$GOPATH/bin"),
        },
        # shell=False, # keep false if possible.
        check=True,
    )


# Conflicting dependencies and blows up on simple scan.
# def run_truffle_hog() -> None:
#     """
#     Run truffle hog command
#     """
#     # need to get the URL from 'git remote show origin'
#     command = (
#         "trufflehog --entropy False "
#         "ssh://.git"
#     )
#     print(command)


# FAST. FATAL ERRORS. DON'T CHANGE THINGS THAT CHECK IN
@task(mypy, detect_secrets, git_secrets, check_package, compile_py, dead_code)
@skip_if_no_change("pre_commit_hook")
@timed()
def pre_commit_hook() -> None:
    """
    Everything that could be run as a pre_commit_hook

    Mostly superceded by precheck utility
    """
    # Don't format or update version
    # Don't do slow stuff- discourages frequent check in
    # Run checks that are likely to have FATAL errors, not just sloppy coding.


# Don't break the build, but don't change source tree either.
@task(mypy, detect_secrets, git_secrets, pytest, check_package, compile_py, dead_code)
@skip_if_no_change("pre_push_hook")
@timed()
def pre_push_hook() -> None:
    """
    More stringent checks to run pre-push
    """
    # Don't format or update version
    # Don't do slow stuff- discourages frequent check in
    # Run checks that are likely to have FATAL errors, not just sloppy coding.


@task()
@timed()
def echo(*args: Any, **kwargs: Any) -> None:
    """
    Pure diagnostics
    """
    print(args)
    print(kwargs)


@task(gitchangelog)
@timed()
def reports() -> None:
    """
    Some build tasks can only be read by a human and can't automatically fail a build.
    For example, git activity reports, complexity metric reports and so on.

    TODO:
    Git reformatting - Authors/Contributors, Changelog
    complexity reports - Cure to complexity sometimes worse that the complexity
    coverage,- Human HTML report runs separately from coverage as quality gate
    dupe code & dead code - Unreliable at detecting real problems
    "grades"
    spelling - involves lengthy step of updating dictionary with false positives
    tox - slow test to say if we can safely upgrade to next version of python/dep
    upgrade report - query pypi for new versions
    source reformating - Sphinx docs
    """


# Default task (if specified) is run when no task is specified in the command line
# make sure you define the variable __DEFAULT__ after the task is defined
# A good convention is to define it at the end of the module
# __DEFAULT__ is an optional member

__DEFAULT__ = echo
