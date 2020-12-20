MINIMUM_SCORE = 0

IGNORE_SYNTAX_ERRORS = True
# one liners are often english with <code/> used for styling
ASSUME_ONE_LINER_IS_NOT_CODE = True
MODULE_NAME = "so_module"
TARGET_FOLDER = "../output"
# import more likely to be executable or nontrivial
MUST_HAVE_IMPORTS = False
# a def or class is already re-usable
MUST_HAVE_CONTAINER = False
WRAP_IN_RUN = True
TEXT_AS_COMMENTS = True
GENERATE_REQUIREMENTS_TXT = True
BUMP_TO_PY3 = True
KEEP_ANSWERS_WITH_NO_CODE = False
KEEP_ANSWERS_WITH_THESE_LANGUAGES = ["*"]
INCLUDE_QUESTION_CODE = True

DEFAULT_LANGUAGE = "Python"
# Language guesser needs hints.
POSSIBLE_LANGUAGES = ["Python", "Jupyter Notebook", "Shell"]
