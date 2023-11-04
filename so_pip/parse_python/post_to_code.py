"""
Install one question or post.

Vendorize because I'm not installing it to a venv.
"""

import collections
from typing import Any, Dict, List, Optional, Tuple

from random_names.make_name import number_to_name

from so_pip import settings as settings
from so_pip.cli_clients.external_commands import black, isort, pur, pylint, safety
from so_pip.file_writing import write_as_html, write_as_md, write_as_text
from so_pip.models.code_file_model import CodeFile
from so_pip.models.count_loc_in_post import count_loc, post_has_code
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
from so_pip.settings import KEEP_ANSWERS_WITH_NO_CODE, KEEP_ANSWERS_WITH_NO_DEF_OR_CLASS
from so_pip.support_files.authors import write_authors
from so_pip.support_files.changelog import changelog_for_post
from so_pip.support_files.code_of_conduct import render_code_of_conduct
from so_pip.support_files.license import write_license
from so_pip.support_files.lua_rockspec import create_rockspec
from so_pip.support_files.package_json import create_package_json
from so_pip.support_files.pyproject_toml import create_pytroject_toml
from so_pip.support_files.python_file import make_python_file
from so_pip.support_files.readme_md import create_readme_md
from so_pip.support_files.requirements_for_post import requirements_for_file
from so_pip.support_files.ruby_gemspec import create_gemspec
from so_pip.utils.user_trace import inform


def handle_post(
    output_folder: str,
    package_prefix: str,
    question: Dict[str, Any],
    answers: List[Dict[str, Any]],
    all_in_one: bool,
    answer_revision: Optional[Dict[str, Any]] = None,
    minimum_loc: int = -1,
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

    # Always fetch the question
    # if doing all in one, we
    question_package_name = number_to_name(question["question_id"], package_prefix, "q")
    question_info = map_post_to_code_package_model(
        question,
        question["body"],
        question_package_name,
        f"StackOverflow post #{question['title']}",
        tags=question["tags"],
    )
    python_source_folder = ""
    supporting_files_folder = ""
    i = 0
    name_uniqifier = ""
    all_in_one_folder_created = False
    for post_type, shallow_post in posts:
        if post_type == "answer" and shallow_post["score"] < settings.MINIMUM_SCORE:
            inform(f"Answer lacks minimum score of {settings.MINIMUM_SCORE}...skipping")
            continue

        if post_type == "answer":
            # cache must be imported late! import too early and cache writes to wrong folder
            # pylint: disable=import-outside-toplevel
            from so_pip.api_clients import stackapi_facade as stackapi_client

            post = stackapi_client.get_json_by_answer_id(shallow_post["answer_id"])[
                "items"
            ][0]
        else:
            post = question

        loc = count_loc(post)
        if loc < minimum_loc:
            inform(
                f"Answer lacks minimum lines of code, "
                f"{loc} vs {minimum_loc} ...skipping"
            )
            continue

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

        # if doing all in one, we need the code info, with new code each iteration
        code_info = map_post_to_code_package_model(
            post,
            post["body"],
            module_name,
            f"StackOverflow post #{question['title']}",
            tags=question["tags"],
        )

        if (
            post_type == "answer"
            and not KEEP_ANSWERS_WITH_NO_DEF_OR_CLASS
            and not is_reusable(post["body"])
            and any(_.language == "python" for _ in code_info.code_blocks)
        ):
            # TODO: make this more strict
            inform("Answer lacks def/class, not re-usable...skipping")
            continue

        # Number files so they can be dumped in the same folder for all_in_one
        if not all_in_one:
            i = 0

        # HACK: should initialize in constructor, not here
        code_info.extract_metadata(post)

        if all_in_one and not all_in_one_folder_created:
            # we do this 1x
            supporting_files_folder, python_source_folder = create_package_folder(
                output_folder, module_name, module_name, question_info
            )
            all_in_one_folder_created = True
        else:
            # 1x per post, both q & a
            supporting_files_folder, python_source_folder = create_package_folder(
                output_folder, module_name, module_name, code_info
            )

        if not python_source_folder:
            raise TypeError("Need python_source_folder by here.")

        frequencies = code_info.file_frequencies()

        code_files_written = []
        for code_file in code_info.code_files:
            i += 1
            if all_in_one:
                name_uniqifier = str(i)
            else:
                name_uniqifier = ""
            submodule_path = f"{python_source_folder}/main{name_uniqifier}"
            code_files_written = write_one_code_file(
                code_file, frequencies, i, code_info, submodule_path, joiner=""
            )

        if settings.GENERATE_JUPYTER:
            write_jupyter_notebook(post, code_info, submodule_path)

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
                code_info,
                question,
                post if post_type == "answer" else None,
            )
        # once per.
        if settings.GENERATE_CODE_OF_CONDUCT:
            render_code_of_conduct(supporting_files_folder)

        if "python" in code_files_written:
            python_versions = validate_with_vermin(python_source_folder)
            code_info.minimum_python = python_versions
            print(code_info.minimum_python)

            # extract requirements, pin, check for security issues
            requirements_txt, count = requirements_for_file(
                supporting_files_folder, code_info
            )
            create_pytroject_toml(supporting_files_folder, code_info, question, post)
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
        # could many several languages per post
        if "javascript" in code_files_written:
            create_package_json(supporting_files_folder, code_info, question, post)
        if "lua" in code_files_written:
            create_rockspec(supporting_files_folder, code_info, question, post)
        if "ruby" in code_files_written:
            create_gemspec(supporting_files_folder, code_info, question, post)
    return packages_made


def write_one_code_file(
    code_file: CodeFile,
    frequencies: collections.Counter,
    i: int,
    package_info: CodePackage,
    submodule_path: str,
    joiner: str,
) -> List[str]:
    """Just code to write a python file"""
    if not submodule_path:
        raise TypeError("Need folder")

    languages_written = set()

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
        make_python_file(
            code_file_name,
            long_header=not settings.METADATA_IN_INIT,
            code=code_to_write_joined,
            python_submodule=package_info,
        )

        languages_written.add("python")

    else:
        # Write a different file.
        # Same thing, but different comment symbols and no python improvements
        # Other than AssemblyInfo.cs, I don't know of any ecosystems
        # that have metadata-in-source code pattern.
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
        languages_written.add(code_file.language)

    return list(languages_written)
