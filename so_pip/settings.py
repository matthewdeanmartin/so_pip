"""
Settings, eventually will be docopts
"""
import os

# do we want this question/answer at all?
from so_pip.file_writing import find_file

MINIMUM_SCORE = 0
KEEP_ANSWERS_WITH_NO_CODE = False
KEEP_ANSWERS_WITH_THESE_LANGUAGES = ["*"]

# this pattern won't work once so_pip is pip installed.
TARGET_FOLDER = find_file("../output", __file__)

# {target_folder}/{package_prefix}_{package_name}/{submodule}.py
# so_pip_packages/fizzbuzz_question_forest_cake/

# how to make the module look
# ------------------------
COMMENT_OUT_BAD_PYTHON = True
# one liners are often english with <code/> used for styling
ASSUME_ONE_LINER_IS_NOT_CODE = True
WRAP_IN_RUN = True
TEXT_AS_COMMENTS = True
GENERATE_REQUIREMENTS_TXT = True
BUMP_TO_PY3 = True
IMPORT_STARTS_NEW_FILE = True
METADATA_IN_INIT = True

# parse code stuff (i.e. could be anything)
DEFAULT_LANGUAGE = "Python"
# Language guesser needs hints.
POSSIBLE_LANGUAGES = ["*"]  # "Python", "Jupyter Notebook", "Shell"]

# cli client stuff
RUNNING_IN_VENV = "VIRTUAL_ENV" in os.environ
SHELL = "pipenv run" if not RUNNING_IN_VENV else ""
