"""
Install one question or answer.

Vendorize because I'm not installing it to a venv.
"""

# TODO:
# install question 142
# install answer 142
# install some_randomish_name
# install some_randomish_name==0.2.1

from typing import Any, List

import stackexchange

from so_pip.api_clients.pystackexchange_facade import question_by_id
from so_pip.cli_clients.external_commands import isort, pylint
from so_pip.file_writing import find_file, write_as_html, write_as_md
from so_pip.model import PythonSubmodule
from so_pip.parse_code.write_anything import write_and_format_any_file
from so_pip.parse_python.format_code import write_and_format_python_file
from so_pip.parse_python.make_name import make_up_module_name
from so_pip.parse_python.module_maker import create_module_folder, handle_python_post
from so_pip.parse_python.python_validator import validate_python
from so_pip.parse_python.upgrade_to_py3 import upgrade_file
from so_pip.settings import (
    BUMP_TO_PY3,
    INCLUDE_QUESTION_CODE,
    METADATA_IN_INIT,
    MINIMUM_SCORE,
    TARGET_FOLDER,
)
from so_pip.support_files.changelog import changelog_for_post
from so_pip.support_files.license import write_license
from so_pip.support_files.requirements_for_post import requirements_for_file


def handle_question(
    module_folder: str, question: stackexchange.Question, submodule: PythonSubmodule
) -> List[str]:
    """same as answers, but for 1 question."""
    # unlike answers, if we decide to include the question, we include the question
    # answers, might get filtered out if they're crap/have no code, etc.
    packages_made: List[str] = []
    submodule_name = "question"
    submodule_path = f"{module_folder}/{submodule_name}"
    packages_made.append(submodule_name)
    i = 0
    for code_file in submodule.code_files:
        if not code_file.extension:
            code_file.analyze()
        if not code_file.extension:
            raise TypeError("need extension by this point")
        i += 1
        code_so_far = code_file.preview_final_code()

        submodule.extract_metadata(question)

        code_file.failed_parse, _ = validate_python(code_so_far)
        # Guess the language from code

        code_file.file_name = f"{submodule_path}_{i}_{code_file.extension}"
        metadata = [] if METADATA_IN_INIT else submodule.python_metadata
        headers = submodule.brief_header if METADATA_IN_INIT else submodule.header
        code_to_write = headers + metadata + code_file.to_write()

        wrote_file = write_and_format_python_file(submodule_path, code_to_write)

        if wrote_file and code_file.language == "Python" and BUMP_TO_PY3:
            upgrade_file(submodule_path)

    write_as_html(question, submodule_path)
    write_as_md(question, submodule_path)
    write_license(question, module_folder)
    changelog_for_post(question, module_folder)
    requirements_for_file(module_folder, submodule)
    return packages_made


def import_so(module_name: str, question_id: int) -> List[str]:
    """main entry point"""
    packages_made: List[str] = []
    question = question_by_id(question_id)

    # create module
    output_folder = find_file(TARGET_FOLDER, __file__)

    submodule = handle_python_post(
        question.body, name="module_folder", description=question.title
    )

    if METADATA_IN_INIT:
        metadata_for_init = "\n".join(submodule.header + submodule.python_metadata)
    else:
        metadata_for_init = ""

    module_folder = create_module_folder(output_folder, module_name, metadata_for_init)

    if INCLUDE_QUESTION_CODE:
        packages_made.extend(handle_question(module_folder, question, submodule))

    packages_made.extend(handle_answers(module_folder, question))
    return packages_made


def handle_answers(module_folder: str, question: Any) -> List[str]:
    """Loop through answers"""
    packages_made: List[str] = []
    for answer in question.answers:
        if answer.score < MINIMUM_SCORE:
            continue
        # answer_module_name = f"answer_{answer.id}"
        answer_module_name = make_up_module_name(answer.id)
        packages_made.append(answer_module_name)
        # TODO: assumes we already know the language & that we are 1 file, 1 language
        submodule = handle_python_post(
            answer.body, answer_module_name, f"StackOverflow answer #{answer.id}"
        )

        # need language for each code file
        # if (
        #     "*" not in KEEP_ANSWERS_WITH_THESE_LANGUAGES
        #     and language not in KEEP_ANSWERS_WITH_THESE_LANGUAGES
        # ):
        #     continue

        i = 0
        submodule.extract_metadata(answer)
        if METADATA_IN_INIT:
            metadata_for_init = "\n".join(submodule.header + submodule.python_metadata)
        else:
            metadata_for_init = ""
        answer_folder = create_module_folder(
            module_folder, answer_module_name, metadata_for_init
        )
        wrote_py_file = False

        submodule_path = f"{module_folder}/{answer_module_name}/main"
        for code_file in submodule.code_files:
            i += 1
            file_header = (
                submodule.brief_header if METADATA_IN_INIT else submodule.header
            )
            code_file_name = f"{submodule_path}_{i}{code_file.extension}"
            to_write = code_file.to_write()
            if code_file.extension == ".py":
                metadata = [] if METADATA_IN_INIT else submodule.python_metadata
                code_to_write = file_header + metadata + to_write
                wrote_py_file = write_and_format_python_file(
                    code_file_name,
                    code_to_write,
                )
                if wrote_py_file and code_file.language == "Python" and BUMP_TO_PY3:
                    upgrade_file(submodule_path)
            else:
                headers = (
                    submodule.brief_header if METADATA_IN_INIT else submodule.header
                )
                code_to_write = headers + to_write
                write_and_format_any_file(
                    code_file_name,
                    code_to_write,
                )

        write_as_html(answer, f"{answer_folder}/answer")
        write_as_md(answer, f"{answer_folder}/answer")
        write_license(answer, answer_folder)
        changelog_for_post(answer, answer_folder)

        # process_requirements_for_a_module(module_folder)
        if wrote_py_file:
            requirements_for_file(answer_folder, submodule)
            isort(module_folder)
            lint_file_name = answer_folder + "/lint.txt"
            with open(lint_file_name, "w", errors="replace") as lint_writer:
                lint_writer.write(pylint(answer_folder))
    return packages_made
