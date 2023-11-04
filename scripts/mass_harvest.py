"""
Gather lots of answers, lots of questions, put all into one folder.

Same as "all in one" workflow except more than one question.
"""
import so_pip.settings as settings
from so_pip.models.count_loc_in_post import post_has_code, count_loc
from so_pip.utils.files_utils import find_file

settings.OUTPUT_FOLDER = find_file("../../output/unittest/", __file__)

if __name__ == "__main__":
    from so_pip.api_clients.stackapi_facade import get_json_by_advanced_search

    for page in range(1, 5000):
        results = get_json_by_advanced_search("", tagged=["python", "boto"], page=page)
        for result in results["items"]:
            body = result["body"]
            if post_has_code(result) and count_loc(result) > 15:
                print(result)
