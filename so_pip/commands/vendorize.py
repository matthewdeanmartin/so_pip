"""
Install one question or post.

Vendorize because I'm not installing it to a venv.
"""

# TODO:
# install question 142
# install post 142
# install some_random_name
# install some_random_name==0.2.1

from typing import Any, Dict, Iterable, List, Tuple

from so_pip import settings as settings
from so_pip.api_clients import stackapi_facade as stackapi_client
from so_pip.cli_clients.external_commands import black, isort, pur, pylint, safety
from so_pip.file_writing import write_as_html, write_as_md, write_as_text
from so_pip.models.python_package_model import PythonPackage
from so_pip.parse_code.write_anything import write_and_format_any_file
from so_pip.parse_python.format_code import write_and_format_python_file
from so_pip.parse_python.make_name import make_up_module_name
from so_pip.parse_python.module_maker import create_package_folder, handle_python_post
from so_pip.parse_python.python_validator import validate_python
from so_pip.parse_python.upgrade_to_py3 import upgrade_file
from so_pip.settings import KEEP_ANSWERS_WITH_NO_CODE
from so_pip.support_files.authors import write_authors
from so_pip.support_files.changelog import changelog_for_post
from so_pip.support_files.code_of_conduct import render_code_of_conduct
from so_pip.support_files.license import write_license
from so_pip.support_files.readme_md import create_readme_md
from so_pip.support_files.requirements_for_post import requirements_for_file


def handle_question(
    package_name: str,
    support_files_path: str,
    python_source_path: str,
    question: Dict[str, Any],
    submodule: PythonPackage,
) -> List[str]:
    """same as answers, but for 1 question."""
    # unlike answers, if we decide to include the question, we include the question
    # answers, might get filtered out if they're crap/have no code, etc.
    packages_made: List[str] = [package_name]

    # submodule_path = f"{module_folder}/{submodule_name}/{submodule_name}"
    # support_files_path =f"{module_folder}/{submodule_name}/"
    i = 0
    for code_file in submodule.code_files:
        if not code_file.extension:
            code_file.analyze(question["tags"])
        if not code_file.extension:
            raise TypeError("need extension by this point")
        i += 1
        code_so_far = code_file.preview_final_code()

        submodule.extract_metadata(question)

        code_file.failed_parse, _ = validate_python(code_so_far)
        # Guess the language from code

        code_file.file_name = f"{python_source_path}question_{i}_{code_file.extension}"
        metadata = [] if settings.METADATA_IN_INIT else submodule.python_metadata
        headers = (
            submodule.brief_header if settings.METADATA_IN_INIT else submodule.header
        )

        if code_file.file_name.endswith(".py"):
            code_to_write = headers + metadata + code_file.to_write()

            wrote_file = write_and_format_python_file(
                code_file.file_name, code_to_write
            )

            if wrote_file and code_file.language == "python" and settings.BUMP_TO_PY3:
                upgrade_file(python_source_path)
        else:
            headers = (
                submodule.brief_header
                if settings.METADATA_IN_INIT
                else submodule.header
            )
            code_to_write = headers + code_file.to_write()
            write_and_format_any_file(
                code_file.file_name,
                code_to_write,
            )

    if settings.POSTS_AS_HTML:
        write_as_html(question, support_files_path)
    if settings.POSTS_AS_MD:
        write_as_md(question, support_files_path)
    if settings.POSTS_AS_TXT:
        write_as_text(question, support_files_path)

    write_license(question, support_files_path)
    if settings.GENERATE_CHANGE_LOG:
        changelog_for_post(question, support_files_path)
    if settings.GENERATE_AUTHORS:
        write_authors(support_files_path, package_name, question)
    if settings.GENERATE_README:
        create_readme_md(support_files_path, submodule, question)
    if settings.GENERATE_CODE_OF_CONDUCT:
        render_code_of_conduct(support_files_path)

    requirements_txt, count = requirements_for_file(support_files_path, submodule)
    if requirements_txt and count > 0:
        pur(requirements_txt)
        result = safety(requirements_txt)
        print(result)

    return packages_made


def import_so_answer(package_prefix: str, answer_id: int,
                     output_folder:str) -> List[str]:
    """main entry point

    package_prefix - prefix for question and post modules

    All modules will be at same tree level
    """
    packages_made: List[str] = []
    answer_data = stackapi_client.get_json_by_answer_id(answer_id)
    answer = answer_data["items"][0]

    question_id = answer["question_id"]
    question = stackapi_client.get_json_by_question_id(question_id)["items"][0]
    packages_made.extend(
        handle_answers(output_folder, package_prefix, question, [answer])
    )
    return packages_made


def import_so_question(package_prefix: str, question_id: int,
                       output_folder:str) -> List[str]:
    """main entry point

    package_prefix - prefix for question and post modules

    All modules will be at same tree level
    """
    packages_made: List[str] = []
    question = stackapi_client.get_json_by_question_id(question_id)["items"][0]


    (
        supporting_files_folder,
        python_source_folder,
        package_info,
    ) = create_package_for_post(output_folder, package_prefix, question)

    packages_made.extend(
        handle_question(
            package_name=package_info.package_name,
            support_files_path=supporting_files_folder,
            python_source_path=python_source_folder,
            question=question,
            submodule=package_info,
        )
    )

    # answers...
    if question["answers"]:
        packages_made.extend(
            handle_answers(output_folder, package_prefix, question, question["answers"])
        )
    return packages_made


def create_package_for_post(
    output_folder: str,
    package_prefix: str,
    post: Dict[str, Any],
) -> Tuple[str, str, PythonPackage]:
    """
    Create package info and folder for a package.

    Could be question or post.

    Flat folder structure (setup.py along with __init__.py)
    """
    post_type = "a" if hasattr(post, "answer_id") else "q"
    post_id = post["answer_id"] if "answer_id" in post else post["question_id"]
    package_name = make_up_module_name(post_id, package_prefix, post_type)
    package_info = handle_python_post(
        post,
        post["body"],
        name=package_name,
        description=post["title"],
        tags=post["tags"],
    )
    if settings.METADATA_IN_INIT:
        metadata_for_init = "\n".join(
            package_info.header + package_info.python_metadata
        )
    else:
        metadata_for_init = ""
    supporting_files_folder, python_source_folder = create_package_folder(
        output_folder, package_name, package_name, metadata_for_init
    )
    return supporting_files_folder, python_source_folder, package_info


def handle_answers(
    output_folder: str,
    package_prefix: str,
    question: Dict[str, Any],
    answers: Iterable[Dict[str, Any]],
) -> List[str]:
    """Loop through answers"""
    packages_made: List[str] = []

    for shallow_answer in answers:
        if shallow_answer["score"] < settings.MINIMUM_SCORE:
            continue
        answer = stackapi_client.get_json_by_answer_id(shallow_answer["answer_id"])[
            "items"
        ][0]

        def answer_has_code(answer: Dict[str, Any]) -> bool:
            """This will probably get more complicated"""
            return "<code" in answer["body"] and "</code>" in answer["body"]

        if not answer_has_code(answer) and not KEEP_ANSWERS_WITH_NO_CODE:
            continue

        answer_module_name = make_up_module_name(
            answer["answer_id"], package_prefix, "a"
        )
        packages_made.append(answer_module_name)

        submodule = handle_python_post(
            answer,
            answer["body"],
            answer_module_name,
            f"StackOverflow post #{answer['answer_id']}",
            tags=question["tags"],
        )

        i = 0
        submodule.extract_metadata(answer)
        if settings.METADATA_IN_INIT:
            metadata_for_init = "\n".join(submodule.header + submodule.python_metadata)
        else:
            metadata_for_init = ""

        supporting_files_folder, python_source_folder = create_package_folder(
            output_folder, answer_module_name, answer_module_name, metadata_for_init
        )
        wrote_py_file = False

        submodule_path = f"{python_source_folder}/main"

        frequencies = submodule.file_frequencies()
        for code_file in submodule.code_files:
            i += 1
            file_header = (
                submodule.brief_header
                if settings.METADATA_IN_INIT
                else submodule.header
            )
            if frequencies.get(code_file.extension, 0) > 1:
                code_file_name = f"{submodule_path}_{i}{code_file.extension}"
            else:
                code_file_name = f"{submodule_path}{code_file.extension}"

            to_write = code_file.to_write()
            if code_file.extension == ".py":
                metadata = (
                    [] if settings.METADATA_IN_INIT else submodule.python_metadata
                )
                code_to_write = file_header + metadata + to_write
                wrote_py_file = write_and_format_python_file(
                    code_file_name,
                    code_to_write,
                )
                if (
                    wrote_py_file
                    and code_file.language == "python"
                    and settings.BUMP_TO_PY3
                ):
                    upgrade_file(submodule_path)
            else:
                headers = (
                    submodule.brief_header
                    if settings.METADATA_IN_INIT
                    else submodule.header
                )
                code_to_write = headers + to_write
                write_and_format_any_file(
                    code_file_name,
                    code_to_write,
                )

        if settings.POSTS_AS_HTML:
            write_as_html(answer, f"{supporting_files_folder}/post")

        write_as_md(answer, f"{supporting_files_folder}/post")
        if settings.POSTS_AS_TXT:
            write_as_text(answer, f"{supporting_files_folder}/post")

        write_license(answer, supporting_files_folder)
        if settings.GENERATE_CHANGE_LOG:
            changelog_for_post(answer, supporting_files_folder)
        if settings.GENERATE_AUTHORS:
            write_authors(supporting_files_folder, answer_module_name, question, answer)
        if settings.GENERATE_README:
            create_readme_md(supporting_files_folder, submodule, question, answer)
        if settings.GENERATE_CODE_OF_CONDUCT:
            render_code_of_conduct(supporting_files_folder)

        if wrote_py_file:
            requirements_txt, count = requirements_for_file(
                supporting_files_folder, submodule
            )
            if requirements_txt and count > 0:
                pur(requirements_txt)
                result = safety(requirements_txt)
                print(result)
            isort(output_folder)
            black(output_folder)
            lint_file_name = supporting_files_folder + "/lint.txt"
            with open(
                lint_file_name, "w", encoding="utf-8", errors="replace"
            ) as lint_writer:
                lint_writer.write(pylint(python_source_folder))
    return packages_made
