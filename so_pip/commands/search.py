"""
Do a search, generate modules for the questions & answers returned.
"""
import logging
from typing import List

from so_pip.commands.vendorize import import_so_question
from so_pip.utils import guards as guards
from so_pip.utils.user_trace import inform

LOGGER = logging.getLogger(__name__)


def import_so_search(
    package_prefix: str,
    query: str,
    tags: List[str],
    output_folder: str,
    stop_after: int = -1,
    minimum_loc: int = -1,
) -> List[str]:
    """Fetch questions and answers via a search"""
    guards.must_be_truthy(query, "query required")
    guards.must_be_truthy(output_folder, "output_folder required")
    inform(f"Starting search for '{query}'...")
    LOGGER.info(f"tags : {tags}")
    if not package_prefix:
        package_prefix = ""
    tags.sort()

    # import late
    # pylint: disable=import-outside-toplevel
    from so_pip.api_clients.stackapi_facade import get_json_by_search

    possibles = get_json_by_search(query, tuple(tags))
    all_results = []
    found = 0

    inform(f"Found {len(possibles['items'])} possible answers")
    for possible in possibles["items"]:
        result = import_so_question(
            package_prefix,
            possible["question_id"],
            output_folder,
            minimum_loc=minimum_loc,
        )
        all_results.extend(result)
        found += 1
        if stop_after != -1 and (found > stop_after):
            break
    else:
        # nothing in possibles[items]
        print("No search results for query")
    return all_results


if __name__ == "__main__":
    import_so_search("pymarc", "pymarc", ["python"], "../../output")
