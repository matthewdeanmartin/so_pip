"""
Install one question or post.

Vendorize because I'm not installing it to a venv.
"""

import collections
from typing import Any, Dict, List, Optional, Tuple

from so_pip import settings as settings
from so_pip.cli_clients.external_commands import black, isort, pur, pylint, safety
from so_pip.file_writing import write_as_html, write_as_md, write_as_text
from so_pip.models.code_file_model import CodeFile
from so_pip.models.python_package_model import CodePackage
from so_pip.parse_code.write_anything import write_and_format_any_file
from so_pip.parse_python.make_notebook import write_jupyter_notebook
from so_pip.parse_python.make_reusable import is_reusable
from so_pip.parse_python.module_maker import (
    create_package_folder,
    map_post_to_code_package_model,
)
from so_pip.parse_python.python_validator import validate_with_vermin
from so_pip.parse_python.upgrade_to_py3 import upgrade_file
from random_names.make_name import number_to_name
from so_pip.settings import KEEP_ANSWERS_WITH_NO_CODE, KEEP_ANSWERS_WITH_NO_DEF_OR_CLASS
from so_pip.support_files.authors import write_authors
from so_pip.support_files.changelog import changelog_for_post
from so_pip.support_files.code_of_conduct import render_code_of_conduct
from so_pip.support_files.license import write_license
from so_pip.support_files.pyproject_toml import create_pytroject_toml
from so_pip.support_files.python_file import make_python_file
from so_pip.support_files.readme_md import create_readme_md
from so_pip.support_files.requirements_for_post import requirements_for_file
from so_pip.utils.user_trace import inform


def handle_post(
    output_folder: str,
    package_prefix: str,
    question: Dict[str, Any],
    answers: List[Dict[str, Any]],
    all_in_one: str,
    answer_revision: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Loop through answers"""
    # HACK: still thinking this out
    if answer_revision and len(answers) == 1:
        answers[0]["body"] = answer_revision["body"]
        # BUG: pretty sure body_md is used too?!

    packages_made: List[str] = []

    posts: List[Tuple[str, Dict[str, Any]]] = []

    posts.append(("question", question))

    for data in answers:
        posts.append(("answer", data))

    # this will never be used
    # but if I don't set it, the code analysis thinks
    # that it might never be set.
    package_info = CodePackage("dummy", "dummy")
    python_source_folder = ""
    supporting_files_folder = ""
    i = 0
    answer_info = None
    for post_type, shallow_post in posts:
        if post_type == "answer" and shallow_post["score"] < settings.MINIMUM_SCORE:
            inform(f"Answer lacks minimum score of {settings.MINIMUM_SCORE}...skipping")
            continue

        if post_type == "answer":
            from so_pip.api_clients import stackapi_facade as stackapi_client

            post = stackapi_client.get_json_by_answer_id(shallow_post["answer_id"])[
                "items"
            ][0]
        else:
            post = question

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
            module_name = number_to_name(post["answer_id"], package_prefix, "a")
        else:
            module_name = number_to_name(post["question_id"], package_prefix, "q")

        packages_made.append(module_name)

        if post_type == "answer" and all_in_one:
            answer_info = map_post_to_code_package_model(
                post,
                post["body"],
                module_name,
                f"StackOverflow post #{question['title']}",
                tags=question["tags"],
            )
        elif (post_type == "answer" and all_in_one) or post_type == "question":
            package_info = map_post_to_code_package_model(
                post,
                post["body"],
                module_name,
                f"StackOverflow post #{question['title']}",
                tags=question["tags"],
            )

        if package_info.package_name == "dummy":
            raise TypeError("Need package by this point")

        if (
            post_type == "answer"
            and not KEEP_ANSWERS_WITH_NO_DEF_OR_CLASS
            and not is_reusable(post["body"])
            and any(_.language == "python" for _ in package_info.code_blocks)
        ):
            # TODO: make this more strict
            inform("Answer lacks def/class, not re-usable...skipping")
            continue

        if not all_in_one:
            i = 0

        package_info.extract_metadata(post)

        if (post_type == "answer" and not all_in_one) or post_type == "question":
            supporting_files_folder, python_source_folder = create_package_folder(
                output_folder, module_name, module_name, package_info
            )
        wrote_py_file = False

        if all_in_one and answer_info:
            package_info = answer_info
        if not python_source_folder:
            raise TypeError("Need python_source_folder by here.")

        frequencies = package_info.file_frequencies()
        wrote_py_file = False
        for code_file in package_info.code_files:
            i += 1
            if all_in_one:
                name_uniqifier = str(i)
            else:
                name_uniqifier = ""
            submodule_path = f"{python_source_folder}/main{name_uniqifier}"
            success = write_one_code_file(
                code_file, frequencies, i, package_info, submodule_path, joiner=""
            )
            if success:
                wrote_py_file = True

        if settings.GENERATE_JUPYTER:
            write_jupyter_notebook(post, package_info, submodule_path)

        if post_type == "answer" and all_in_one:
            # TODO: should be like "joes_post"
            supporting_file_name = f"{supporting_files_folder}/post_{i}"
        else:
            supporting_file_name = f"{supporting_files_folder}/post"
        if settings.POSTS_AS_HTML:
            write_as_html(post, supporting_file_name)
        if settings.POSTS_AS_MD:
            write_as_md(post, supporting_file_name)
        if settings.POSTS_AS_TXT:
            write_as_text(post, supporting_file_name)

        write_license(post, supporting_files_folder)

        if settings.GENERATE_CHANGE_LOG:
            changelog_for_post(post, supporting_files_folder, name_uniqifier)
        if settings.GENERATE_AUTHORS:
            write_authors(
                supporting_files_folder,
                module_name,
                question,
                post if post_type == "answer" else None,
                name_uniqifier,
            )
        # once per.
        if settings.GENERATE_README:
            create_readme_md(
                supporting_files_folder,
                package_info,
                question,
                post if post_type == "answer" else None,
            )
        # once per.
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
            lint_file_name = supporting_files_folder + f"/lint{name_uniqifier}.txt"
            with open(
                lint_file_name, "w", encoding="utf-8", errors="replace"
            ) as lint_writer:
                lint_writer.write(pylint(python_source_folder))

    return packages_made


def write_one_code_file(
    code_file: CodeFile,
    frequencies: collections.Counter,
    i: int,
    package_info: CodePackage,
    submodule_path: str,
    joiner: str,
) -> bool:
    """Just code to write a python file"""
    if not submodule_path:
        raise TypeError("Need folder")

    wrote_py_file = False

    if frequencies.get(code_file.extension, 0) > 1:
        code_file_name = f"{submodule_path}_{joiner}{i}{code_file.extension}"
    else:
        code_file_name = f"{submodule_path}{code_file.extension}"

    to_write = code_file.to_write()
    if code_file.extension == ".py":

        code_to_write = to_write
        while code_to_write[-1].strip() in ("", "#"):
            code_to_write.pop()

        code_to_write_joined = "\n".join(code_to_write)
        wrote_py_file = make_python_file(
            code_file_name,
            long_header=settings.METADATA_IN_INIT,
            code=code_to_write_joined,
            python_submodule=package_info,
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
