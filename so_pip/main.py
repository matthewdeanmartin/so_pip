"""
Formalize copy-paste from StackOverflow.

Code generates modules using code found in answers.
"""
import os
from typing import Any

import stackexchange
from dotenv import load_dotenv

from so_pip.changelog import changelog_for_post
from so_pip.external_commands import isort, pylint
from so_pip.file_writing import (
    find_file,
    write_and_format_python_file,
    write_as_html,
    write_as_md,
    write_license,
)
from so_pip.language_guessing import assign_extension
from so_pip.module_maker import create_module_folder, handle_python_answer
from so_pip.requirements_for_post import requirements_for_file
from so_pip.settings import (
    BUMP_TO_PY3,
    INCLUDE_QUESTION_CODE,
    KEEP_ANSWERS_WITH_NO_CODE,
    KEEP_ANSWERS_WITH_THESE_LANGUAGES,
    MINIMUM_SCORE,
    MUST_HAVE_CONTAINER,
    MUST_HAVE_IMPORTS,
    TARGET_FOLDER,
)
from so_pip.upgrade_to_py3 import upgrade_file

load_dotenv()

STACK = stackexchange.Site(stackexchange.StackOverflow, os.environ["key"])


def handle_question(module_folder: str, question: stackexchange.Question) -> None:
    """same as answers, but for 1 question."""
    submodule = handle_python_answer(
        question.body, name="module_folder", description=question.title
    )

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

    wrote_file = False
    if KEEP_ANSWERS_WITH_NO_CODE or submodule.non_comment_lines() > 0:
        if submodule_name.endswith(".py"):
            code_to_write = (
                submodule.header + submodule.python_metadata + submodule.to_write
            )
        else:
            code_to_write = submodule.header + submodule.to_write

        wrote_file = write_and_format_python_file(submodule_name, code_to_write)

    write_as_html(question, submodule_name.replace(extension, ""))
    write_as_md(question, submodule_name.replace(extension, ""))
    write_license(question, module_folder)
    changelog_for_post(question, module_folder)
    if wrote_file and language == "Python":
        if BUMP_TO_PY3:
            upgrade_file(submodule_name)
        requirements_for_file(submodule_name, module_folder, submodule)


def import_so(module_name: str, question_id: int) -> None:
    """main entry point"""
    STACK.include_body = True
    question = STACK.question(question_id)

    # create module
    output_folder = find_file(TARGET_FOLDER, __file__)
    module_folder = create_module_folder(output_folder, module_name)

    if INCLUDE_QUESTION_CODE:
        handle_question(module_folder, question)

    handle_answers(module_folder, question)


def handle_answers(module_folder: str, question: Any) -> None:
    """Loop through answers"""
    for answer in question.answers:
        if answer.score < MINIMUM_SCORE:
            continue
        answer_module_name = f"answer_{answer.id}"
        submodule = handle_python_answer(
            answer.body, answer_module_name, f"StackOverflow answer #{answer.id}"
        )

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

        answer_folder = create_module_folder(module_folder, answer_module_name)
        submodule_path = f"{module_folder}/{answer_module_name}/main{extension}"

        if (
            "*" not in KEEP_ANSWERS_WITH_THESE_LANGUAGES
            and language not in KEEP_ANSWERS_WITH_THESE_LANGUAGES
        ):
            continue
        wrote_py_file = False
        if KEEP_ANSWERS_WITH_NO_CODE or submodule.non_comment_lines() > 0:
            wrote_py_file = write_and_format_python_file(
                submodule_path,
                submodule.header + submodule.python_metadata + submodule.to_write,
            )

        write_as_html(answer, submodule_path.replace(extension, ""))
        write_as_md(answer, submodule_path.replace(extension, ""))
        write_license(answer, answer_folder)
        changelog_for_post(answer, answer_folder)

        # process_requirements_for_a_module(module_folder)
        if wrote_py_file and language == "Python":
            if BUMP_TO_PY3:
                upgrade_file(submodule_path)
            requirements_for_file(submodule_path, answer_folder, submodule)
            isort(module_folder)
            lint_file_name = submodule_path.replace(extension, "") + "_lint.txt"
            with open(lint_file_name, "w", errors="replace") as lint_writer:
                lint_writer.write(pylint(module_folder))
