from so_pip.commands.vendorize import import_so_question, import_so_answer
from so_pip.utils.files_utils import find_file

OUTPUT_FOLDER = find_file("../output", __file__)
if __name__ == "__main__":

    # https://stackoverflow.com/questions/32833797/

    import_so_question(
        "days_between", 151199, OUTPUT_FOLDER
    )  # has interactive e.g. >>>
    # import_so_question("js", 32833797, OUTPUT_FOLDER)
    # import_so_question("cs", 65859313, OUTPUT_FOLDER)
    # import_so_answer("unzip", 1855118, OUTPUT_FOLDER, revision_id=-1)
    # import_so_question("package_for_module", 49764802, OUTPUT_FOLDER)
    exit()
    # import_so_answer("popular", 237028, OUTPUT_FOLDER, 2)  # questoin 231767
    # import_so_question("game_thing", 42742423, OUTPUT_FOLDER)
    # import_so_answer("find_imports", 18812776, OUTPUT_FOLDER, -1)
    # import_so_answer("import_vendor", 2572654, OUTPUT_FOLDER,-1)

    import_so_question("detect_tests", 14405063, OUTPUT_FOLDER)
    # https://stackoverflow.com/questions/13137817/
    # how-to-download-image-using-requests
    import_so_question(
        "requests_help", 13137817, OUTPUT_FOLDER
    )  # requests, excellent example

    # #
    # # import_so_question("django", 15029666)
    # # https://stackoverflow.com/questions/40476966/python-text-adventure-items-interacting-with-the-game-world
    import_so_question("game", 40476966, OUTPUT_FOLDER)
    #
    # # https://stackoverflow.com/questions/54290362/
    # #how-to-write-a-simple-blockchain-in-python
    # import_so_question("blockchain_nocode", 54290362)  # no code!
    #
    # import_so_question("idenitfy_py2", 38604451)  # has negative post
    # # https://stackoverflow.com/questions/151199/
    # #how-to-calculate-number-of-days-between-two-given-dates

    # # https://stackoverflow.com/questions/7586063/
    # #how-to-calculate-the-angle-between-a-line-and-the-horizontal-axis
    # import_so_question("angle_calc", 7586063)
    # # https://stackoverflow.com/questions/31684375/
    # #automatically-create-requirements-txt
    # import_so_question("requirements_from_text", 31684375)
    # # https://stackoverflow.com/questions/7065164/
    # #how-to-make-an-unaware-datetime-timezone-aware-in-python
    # import_so_question("time_zone_aware", 7065164)
    # # https://stackoverflow.com/questions/466345/
    # #converting-string-into-datetime/466376#466376
    # import_so_question("string_to_date", 466345)
    # #https://stackoverflow.com/questions/3894265/
    # #example-function-in-python-counting-words
    # import_so_question("count_words", 3894265)
    # #https://stackoverflow.com/questions/65373654/
    # # cant-figure-out-how-to-check-my-list-and-input-with-each-other
    # # question matters
    # import_so_question("question_matters", 65373654)
    # # https://stackoverflow.com/questions/22743860/python-fizzbuzz
    # import_so_question("fizzbuzz", 22743860)
    # import_so_question("find_imports_better", 9008451)
    # import_so_question("question_matters", 65373654)
    # # # https://stackoverflow.com/questions/2572582/return-a-list-of-imported-python-modules-used-in-a-script
    # import_so_question("find_imports", 2572582)
    # # # has fiddle, strong evidence of working code
    # # # https://stackoverflow.com/questions/5874652/prop-vs-attr
    # # 24139250
    # import_so_question("pyso_answers_by_user", 24139250)
