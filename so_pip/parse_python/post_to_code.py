"""
Install one question or post.

Vendorize because I'm not installing it to a venv.
"""

import collections
from typing import Any, Dict, List, Optional, Tuple

from so_pip import settings as settings
from so_pip.api_clients import stackapi_facade as stackapi_client
from so_pip.cli_clients.external_commands import black, isort, pur, pylint, safety
from so_pip.file_writing import write_as_html, write_as_md, write_as_text
from so_pip.models.code_file_model import CodeFile
from so_pip.models.python_package_model import PythonPackage
from so_pip.parse_code.write_anything import write_and_format_any_file
from so_pip.parse_python.format_code import write_and_format_python_file
from so_pip.parse_python.make_reusable import is_reusable
from so_pip.parse_python.module_maker import (
    create_package_folder,
    map_post_to_python_package_model,
)
from so_pip.parse_python.python_validator import validate_with_vermin
from so_pip.parse_python.upgrade_to_py3 import upgrade_file
from so_pip.random_names.make_name import make_up_module_name
from so_pip.settings import KEEP_ANSWERS_WITH_NO_CODE, KEEP_ANSWERS_WITH_NO_DEF_OR_CLASS
from so_pip.support_files.authors import write_authors
from so_pip.support_files.changelog import changelog_for_post
from so_pip.support_files.code_of_conduct import render_code_of_conduct
from so_pip.support_files.license import write_license
from so_pip.support_files.pyproject_toml import create_pytroject_toml
from so_pip.support_files.readme_md import create_readme_md
from so_pip.support_files.requirements_for_post import requirements_for_file
from so_pip.utils.user_trace import inform


def handle_post(
    output_folder: str,
    package_prefix: str,
    question: Dict[str, Any],
    answers: List[Dict[str, Any]],
    answer_revision: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Loop through answers"""
    # HACK: still thinking this out
    if answer_revision and len(answers) == 1:
        answers[0]["body"] = answer_revision["body"]
        # BUG: pretty sure body_md is used too?!

    packages_made: List[str] = []

    posts: List[Tuple[str, Dict[str, Any]]] = []
    for data in answers:
        posts.append(("answer", data))

    # TODO: switch for if we include Q
    posts.append(("question", question))

    for post_type, shallow_post in posts:
        if post_type == "answer" and shallow_post["score"] < settings.MINIMUM_SCORE:
            inform(f"Answer lacks minimum score of {settings.MINIMUM_SCORE}...skipping")
            continue

        if post_type == "answer":
            post = stackapi_client.get_json_by_answer_id(shallow_post["answer_id"])[
                "items"
            ][0]
        else:
            post = question

        if (
            post_type == "answer"
            and not KEEP_ANSWERS_WITH_NO_DEF_OR_CLASS
            and not is_reusable(post["body"])
        ):
            # TODO: make this more strict
            inform("Answer lacks def/class, not re-usable...skipping")
            continue

        def post_has_code(answer: Dict[str, Any]) -> bool:
            """This will probably get more complicated"""
            return "<pre><code" in answer["body"] and "</code>" in answer["body"]

        if (
            not post_has_code(post)
            and not KEEP_ANSWERS_WITH_NO_CODE
            and post_type == "answer"
        ):
            inform("Answer lacks code blocks,...skipping")
            continue

        if post_type == "answer":
            module_name = make_up_module_name(post["answer_id"], package_prefix, "a")
        else:
            module_name = make_up_module_name(post["question_id"], package_prefix, "q")
        packages_made.append(module_name)

        package_info = map_post_to_python_package_model(
            post,
            post["body"],
            module_name,
            f"StackOverflow post #{question['title']}",
            tags=question["tags"],
        )

        i = 0
        package_info.extract_metadata(post)
        if settings.METADATA_IN_INIT:
            metadata_for_init = "\n".join(
                package_info.header + package_info.python_metadata
            )
        else:
            metadata_for_init = ""

        supporting_files_folder, python_source_folder = create_package_folder(
            output_folder, module_name, module_name, metadata_for_init
        )
        wrote_py_file = False

        submodule_path = f"{python_source_folder}/main"

        frequencies = package_info.file_frequencies()
        for code_file in package_info.code_files:
            i += 1
            success = write_one_python_file(
                code_file, frequencies, i, package_info, submodule_path, joiner=""
            )
            if success:
                wrote_py_file = True

        if settings.POSTS_AS_HTML:
            write_as_html(post, f"{supporting_files_folder}/post")
        if settings.POSTS_AS_MD:
            write_as_md(post, f"{supporting_files_folder}/post")
        if settings.POSTS_AS_TXT:
            write_as_text(post, f"{supporting_files_folder}/post")

        write_license(post, supporting_files_folder)
        if settings.GENERATE_CHANGE_LOG:
            changelog_for_post(post, supporting_files_folder)
        if settings.GENERATE_AUTHORS:
            write_authors(
                supporting_files_folder,
                module_name,
                question,
                post if post_type == "answer" else None,
            )
        if settings.GENERATE_README:
            create_readme_md(
                supporting_files_folder,
                package_info,
                question,
                post if post_type == "answer" else None,
            )
        if settings.GENERATE_CODE_OF_CONDUCT:
            render_code_of_conduct(supporting_files_folder)

        if wrote_py_file:
            python_versions = validate_with_vermin(python_source_folder)
            package_info.minimum_python = python_versions
            print(package_info.minimum_python)

            # extract requirements, pin, check for security issues
            requirements_txt, count = requirements_for_file(
                supporting_files_folder, package_info
            )
            create_pytroject_toml(supporting_files_folder, package_info, question, post)
            if requirements_txt and count > 0:
                pur(requirements_txt)
                result = safety(requirements_txt)
                inform(result)
            # Upgrade, but this is one of the slower things to do.
            # Also, eval(input()) makes things worse.
            if settings.BUMP_TO_PY3:
                upgrade_file(submodule_path)
            # format
            isort(output_folder)
            black(output_folder)
            # lint
            lint_file_name = supporting_files_folder + "/lint.txt"
            with open(
                lint_file_name, "w", encoding="utf-8", errors="replace"
            ) as lint_writer:
                lint_writer.write(pylint(python_source_folder))

    return packages_made


def write_one_python_file(
    code_file: CodeFile,
    frequencies: collections.Counter,
    i: int,
    package_info: PythonPackage,
    submodule_path: str,
    joiner: str,
) -> bool:
    """Just code to write a python file"""
    wrote_py_file = False
    file_header = (
        package_info.brief_header if settings.METADATA_IN_INIT else package_info.header
    )
    if frequencies.get(code_file.extension, 0) > 1:
        code_file_name = f"{submodule_path}_{joiner}{i}{code_file.extension}"
    else:
        code_file_name = f"{submodule_path}{code_file.extension}"
    to_write = code_file.to_write()
    if code_file.extension == ".py":
        metadata = [] if settings.METADATA_IN_INIT else package_info.python_metadata
        code_to_write = file_header + metadata + to_write
        wrote_py_file = write_and_format_python_file(
            code_file_name,
            code_to_write,
        )

    else:
        # Write a different file.
        # Same thing, but different comment symbols and no python improvements
        headers = (
            package_info.brief_header
            if settings.METADATA_IN_INIT
            else package_info.header
        )
        code_to_write = headers + to_write
        write_and_format_any_file(
            code_file_name,
            code_to_write,
        )
    return wrote_py_file
