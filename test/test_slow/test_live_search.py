import so_pip.settings as settings
from so_pip.commands.search import import_so_search
from so_pip.utils.files_utils import find_file

settings.OUTPUT_FOLDER = find_file("../../output/unittest/", __file__)

# doesn't support  is:answer in query!
# GET search endpoint is rotten!
# Only "intitle" so can't search if body has def/class! (i.e. basic units of re-usability)

def test_import_so_search():
    result = import_so_search(
        package_prefix="test",
        query="aws",
        tags=["python"],
        output_folder=settings.OUTPUT_FOLDER,
        stop_after=2,
        minimum_loc=15
    )
    print(result)
    assert result
