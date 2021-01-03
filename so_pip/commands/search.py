"""
Do a search, generate modules for the questions & answers returned.
"""
from typing import List

from so_pip.api_clients.stackapi_facade import get_json_by_search
from so_pip.commands.vendorize import import_so_question
from so_pip.utils import guards as guards
from so_pip.utils.user_trace import inform


def import_so_search(
    package_prefix: str,
    query: str,
    tags: List[str],
    output_folder: str,
    stop_after: int = -1,
) -> List[str]:
    """Fetch questions and answers via a search"""
    guards.must_be_truthy(query, "query required")
    guards.must_be_truthy(output_folder, "output_folder required")
    inform(f"Starting search for '{query}'...")
    if not package_prefix:
        package_prefix = ""
    tags.sort()
    possibles = get_json_by_search(query, tuple(tags))
    all_results = []
    found = 0
    for possible in possibles["items"]:
        result = import_so_question(
            package_prefix, possible["question_id"], output_folder
        )
        all_results.extend(result)
        found += 1
        if stop_after != -1 and (found > stop_after):
            break
    return all_results


if __name__ == "__main__":
    import_so_search("pymarc", "pymarc", ["python"], "../../output")
