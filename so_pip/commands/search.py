"""
Do a search, generate modules for the questions & answers returned.
"""
from typing import List

from so_pip.api_clients.stackapi_facade import get_json_by_search
from so_pip.commands.vendorize import import_so_question


def import_so_search(package_prefix: str, query: str, tags:List[str], stop_after:int=-1) -> List[str]:
    possibles = get_json_by_search(query, tags)
    all_results=[]
    found = 0
    for possible in possibles["items"]:
        result = import_so_question(package_prefix, possible["question_id"])
        all_results.extend(result)
        found +=1
        if stop_after!=-1 and found>stop_after:
             break
    return all_results


if __name__ == "__main__":
    import_so_search("pymarc", "pymarc", ["python"])
