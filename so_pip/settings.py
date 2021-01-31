"""
Settings, eventually will be docopts
"""
import ast

# do we want this question/post at all?
import configparser
import os
from typing import Tuple, cast

from so_pip.utils.files_utils import find_file

if os.path.exists(".so_pip.ini"):
    # exist where user executes from.
    CONFIG_PATH = ".so_pip.ini"
else:
    # unit tests, etc.
    CONFIG_PATH = find_file("../.so_pip.ini", __file__)
if os.path.exists(CONFIG_PATH):
    print(f"Loading config from {CONFIG_PATH}")
    config = configparser.ConfigParser()
    result = config.read(CONFIG_PATH)
else:
    print("Did not fine a .so_pip.ini file anywhere, using default behaviors.")
    # duck typing
    config = cast(configparser.ConfigParser, configparser.RawConfigParser())
    config.add_section("POST_FILTERS")
    config.add_section("VENDORIZING")
    config.add_section("CODE_CLEANUP")
    config.add_section("SUPPORTING_FILES")
    config.add_section("LANGUAGE_DETECTION")
    config.add_section("SHELL_CONFIG")

section = config["POST_FILTERS"]
MINIMUM_SCORE = ast.literal_eval(section.get("MINIMUM_SCORE", "0"))
KEEP_ANSWERS_WITH_NO_CODE = ast.literal_eval(
    section.get("KEEP_ANSWERS_WITH_NO_CODE", "False")
)
KEEP_ANSWERS_WITH_NO_DEF_OR_CLASS = ast.literal_eval(
    section.get("KEEP_ANSWERS_WITH_NO_CODE", "False")
)

# this pattern won't work once so_pip is pip installed.
section = config["VENDORIZING"]

# {target_folder}/{package_prefix}_{package_name}/{package_info}.py
# so_pip_packages/fizzbuzz_question_forest_cake/

# how to make the module look
# ------------------------
section = config["CODE_CLEANUP"]
# one liners are often english with <code/> used for styling
ASSUME_ONE_LINER_IS_NOT_CODE = ast.literal_eval(
    section.get("ASSUME_ONE_LINER_IS_NOT_CODE", "True")
)
CODE_IN_SRC_FOLDER = ast.literal_eval(section.get("CODE_IN_SRC_FOLDER", "False"))

# python stuff
PYTHON_CODE_IN_MODULE_FOLDER = ast.literal_eval(
    section.get("PYTHON_CODE_IN_MODULE_FOLDER", "False")
)
COMMENT_OUT_BAD_PYTHON = ast.literal_eval(
    section.get("COMMENT_OUT_BAD_PYTHON", "False")
)
WRAP_IN_RUN = ast.literal_eval(section.get("WRAP_IN_RUN", "False"))
# Slow but necessary because so many answers are old.
BUMP_TO_PY3 = ast.literal_eval(section.get("BUMP_TO_PY3", "True"))
IMPORT_STARTS_NEW_FILE = ast.literal_eval(section.get("IMPORT_STARTS_NEW_FILE", "True"))

section = config["SUPPORTING_FILES"]
# stackover flow stuff
POSTS_AS_TXT = ast.literal_eval(section.get("POSTS_AS_TXT", "True"))
POSTS_AS_HTML = ast.literal_eval(section.get("POSTS_AS_HTML", "True"))
POSTS_AS_MD = ast.literal_eval(section.get("POSTS_AS_MD", "True"))

# python stuff
CODE_IN_SRC_FOLDER = ast.literal_eval(section.get("CODE_IN_SRC_FOLDER", "True"))
METADATA_IN_INIT = ast.literal_eval(section.get("METADATA_IN_INIT", "True"))
GENERATE_REQUIREMENTS_TXT = ast.literal_eval(
    section.get("GENERATE_REQUIREMENTS_TXT", "True")
)
GENERATE_JUPYTER = ast.literal_eval(section.get("GENERATE_JUPYTER", "True"))

# gnits stuff
GENERATE_AUTHORS = ast.literal_eval(section.get("GENERATE_AUTHORS", "True"))
GENERATE_README = ast.literal_eval(section.get("GENERATE_README", "True"))
GENERATE_CODE_OF_CONDUCT = ast.literal_eval(
    section.get("GENERATE_CODE_OF_CONDUCT", "True")
)
GENERATE_CHANGE_LOG = ast.literal_eval(section.get("GENERATE_CHANGE_LOG", "True"))
GENERATE_SETUP_CFG = ast.literal_eval(section.get("GENERATE_SETUP_CFG", "True"))

section = config["LANGUAGE_DETECTION"]
DEFAULT_LANGUAGE = cast(
    Tuple[str, str],
    ast.literal_eval(section.get("DEFAULT_LANGUAGE", "('.py', 'python')")),
)

# Language guesser needs hints.
# Default hints for python and javascript because
# those languages now (or will) have more support for extracting a package.
POSSIBLE_LANGUAGES = ast.literal_eval(
    section.get("POSSIBLE_LANGUAGES", "['python','javascript','lua']")
)

# cli client stuff
section = config["SHELL_CONFIG"]
RUNNING_IN_VENV = "VIRTUAL_ENV" in os.environ
SHELL = section.get("SHELL", "") if not RUNNING_IN_VENV else ""
QUIET = False

OUTPUT_FOLDER = ""
