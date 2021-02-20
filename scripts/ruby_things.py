"""
Ruby
"""
# @ https://stackoverflow.com/a/12927726/33264

from so_pip.commands.vendorize import import_so_question, import_so_answer
from so_pip.utils.files_utils import find_file

OUTPUT_FOLDER = find_file("../output", __file__)
if __name__ == "__main__":
    # 34897423/33264
    import_so_answer("ecs", 34897423, OUTPUT_FOLDER, revision_id=None)
