"""
Formalize copy-paste from StackOverflow.

Code generates modules using code found in answers.
"""
import os
import subprocess  # nosec
from typing import List, Any

import stackexchange
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from so_pip.code_transformations import (
    fix_interactive,
    fix_shell,
    html_to_python_comments,
)
from so_pip.external_commands import generate_requirements, isort
from so_pip.file_writing import create_module_folder, write_as_html, write_to_file
from so_pip.language_guessing import assign_extension
from so_pip.model import PythonSubmodule
from so_pip.module_maker import handle_python_answer
from so_pip.python_validator import validate_python
from so_pip.settings import (
    ASSUME_ONE_LINER_IS_NOT_CODE,
    BUMP_TO_PY3,
    GENERATE_REQUIREMENTS_TXT,
    IGNORE_SYNTAX_ERRORS,
    KEEP_ANSWERS_WITH_NO_CODE,
    KEEP_ANSWERS_WITH_THESE_LANGUAGES,
    MINIMUM_SCORE,
    MUST_HAVE_CONTAINER,
    MUST_HAVE_IMPORTS,
    TARGET_FOLDER, INCLUDE_QUESTION_CODE,
)
from so_pip.upgrade_to_py3 import upgrade_file, upgrade_string

load_dotenv()

STACK = stackexchange.Site(stackexchange.StackOverflow, os.environ["key"])


def handle_question(module_folder:str, question:Any)->None:
    """same as answers, but for 1 question."""
    submodule = handle_python_answer(question.body)

    code_so_far = submodule.preview_final_code()
    if MUST_HAVE_IMPORTS and "import" not in code_so_far:
        return
    if MUST_HAVE_CONTAINER and (
        "def " not in code_so_far and "class" not in code_so_far
    ):
        return

    submodule.handle_header(question)

    # Guess the language from code
    extension, language = assign_extension(code_so_far, submodule.failed_parse)
    submodule_name = f"{module_folder}/question{extension}"

    if (
        "*" not in KEEP_ANSWERS_WITH_THESE_LANGUAGES
        and language not in KEEP_ANSWERS_WITH_THESE_LANGUAGES
    ):
        return

    if KEEP_ANSWERS_WITH_NO_CODE or submodule.non_comment_lines() > 0:
        write_to_file(submodule_name, submodule.header + submodule.to_write)

    write_as_html(question, submodule_name)
    if BUMP_TO_PY3 and language == "Python":
        upgrade_file(submodule_name)


def import_so(module_name: str, question_id: int) -> None:
    """main entry point"""
    STACK.include_body = True
    question = STACK.question(question_id)

    # create module
    module_folder = create_module_folder(TARGET_FOLDER, module_name)

    if INCLUDE_QUESTION_CODE:
        handle_question(module_folder, question)

    handle_answers(module_folder, question)


    if GENERATE_REQUIREMENTS_TXT:
        try:
            generate_requirements(module_folder, "pipenv run")
        except subprocess.CalledProcessError as cpe:
            print(f"generate requirements failed : {module_folder}", str(cpe))
    isort("../output", "pipenv run")


def handle_answers(module_folder:str, question:Any)->None:
    """Loop through answers"""
    for answer in question.answers:
        if answer.score < MINIMUM_SCORE:
            continue

        submodule = handle_python_answer(answer.body)

        code_so_far = submodule.preview_final_code()
        if MUST_HAVE_IMPORTS and "import" not in code_so_far:
            continue
        if MUST_HAVE_CONTAINER and (
            "def " not in code_so_far and "class" not in code_so_far
        ):
            continue

        submodule.handle_header(answer)

        # Guess the language from code
        extension, language = assign_extension(code_so_far, submodule.failed_parse)
        submodule_name = f"{module_folder}/answer_{answer.id}{extension}"

        if (
            "*" not in KEEP_ANSWERS_WITH_THESE_LANGUAGES
            and language not in KEEP_ANSWERS_WITH_THESE_LANGUAGES
        ):
            continue

        if KEEP_ANSWERS_WITH_NO_CODE or submodule.non_comment_lines() > 0:
            write_to_file(submodule_name, submodule.header + submodule.to_write)

        write_as_html(answer, submodule_name)
        if BUMP_TO_PY3 and language == "Python":
            upgrade_file(submodule_name)



