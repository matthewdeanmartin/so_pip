"""
Settings, eventually will be docopts
"""
import ast

# do we want this question/post at all?
import configparser
import os
from typing import Tuple, cast

from so_pip.utils.files_utils import find_file

config = configparser.ConfigParser()
if os.path.exists(".so_pip.ini"):
    # exist where user executes from.
    CONFIG_PATH = ".so_pip.ini"
else:
    # unit tests, etc.
    CONFIG_PATH = find_file("../.so_pip.ini", __file__)
print(f"Loading config from {CONFIG_PATH}")
result = config.read(CONFIG_PATH)

section = config["POST_FILTERS"]
MINIMUM_SCORE = ast.literal_eval(section["MINIMUM_SCORE"])
KEEP_ANSWERS_WITH_NO_CODE = ast.literal_eval(section["KEEP_ANSWERS_WITH_NO_CODE"])
KEEP_ANSWERS_WITH_THESE_LANGUAGES = ast.literal_eval(
    section["KEEP_ANSWERS_WITH_THESE_LANGUAGES"]
)

# this pattern won't work once so_pip is pip installed.
section = config["VENDORIZING"]
# TODO
TARGET_FOLDER = find_file("../output", __file__)

# {target_folder}/{package_prefix}_{package_name}/{submodule}.py
# so_pip_packages/fizzbuzz_question_forest_cake/

# how to make the module look
# ------------------------
section = config["CODE_CLEANUP"]
COMMENT_OUT_BAD_PYTHON = ast.literal_eval(section["COMMENT_OUT_BAD_PYTHON"])
# one liners are often english with <code/> used for styling
ASSUME_ONE_LINER_IS_NOT_CODE = ast.literal_eval(section["ASSUME_ONE_LINER_IS_NOT_CODE"])
WRAP_IN_RUN = ast.literal_eval(section["WRAP_IN_RUN"])
TEXT_AS_COMMENTS = ast.literal_eval(section["TEXT_AS_COMMENTS"])
BUMP_TO_PY3 = ast.literal_eval(section["BUMP_TO_PY3"])
IMPORT_STARTS_NEW_FILE = ast.literal_eval(section["IMPORT_STARTS_NEW_FILE"])

section = config["SUPPORTING_FILES"]
POSTS_AS_TXT = ast.literal_eval(section["POSTS_AS_TXT"])
POSTS_AS_HTML = ast.literal_eval(section["POSTS_AS_HTML"])
POSTS_AS_MD = ast.literal_eval(section["POSTS_AS_MD"])
METADATA_IN_INIT = ast.literal_eval(section["METADATA_IN_INIT"])
GENERATE_REQUIREMENTS_TXT = ast.literal_eval(section["GENERATE_REQUIREMENTS_TXT"])
GENERATE_AUTHORS = ast.literal_eval(section["GENERATE_AUTHORS"])
GENERATE_README = ast.literal_eval(section["GENERATE_README"])
GENERATE_CODE_OF_CONDUCT = ast.literal_eval(section["GENERATE_CODE_OF_CONDUCT"])
GENERATE_CHANGE_LOG = ast.literal_eval(section["GENERATE_CHANGE_LOG"])
SETUP_CFG_OR_SETUP_PY = section["SETUP_CFG_OR_SETUP_PY"]


section = config["LANGUAGE_DETECTION"]
DEFAULT_LANGUAGE = cast(Tuple[str, str], ast.literal_eval(section["DEFAULT_LANGUAGE"]))
# Language guesser needs hints.
POSSIBLE_LANGUAGES = ast.literal_eval(section["DEFAULT_LANGUAGE"])

# cli client stuff
section = config["SHELL_CONFIG"]
RUNNING_IN_VENV = "VIRTUAL_ENV" in os.environ
SHELL = section["SHELL"] if not RUNNING_IN_VENV else ""
