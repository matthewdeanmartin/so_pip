
from so_pip.api_clients.stackapi_facade import get_json_by_question_id, \
    get_json_by_answer_id
from so_pip.parse_python.module_maker import handle_python_post



def test_handle_python_answer():
    answer = get_json_by_answer_id(24139629)["items"][0]
    question = get_json_by_question_id(answer["question_id"])["items"][0]
    submodule = handle_python_post(
            answer["body"], "answer_module_name", f"StackOverflow answer #{answer['answer_id']}",
            question["tags"]
        )
    assert submodule.code_blocks
    assert submodule.code_files
    assert sum(len(file.code_blocks) for file in submodule.code_files)==len(submodule.code_blocks)
    for file in submodule.code_files:
        assert file.extension


def test_handle_python_question():
    value = get_json_by_question_id(24139250)["items"][0]
    submodule = handle_python_post(
        value["body"], "answer_module_name", f"StackOverflow answer #{value['question_id']}",
        value["tags"]
    )
    assert submodule.code_blocks
    assert submodule.code_files
    assert sum(len(file.code_blocks) for file in submodule.code_files) == len(
        submodule.code_blocks)
    for file in submodule.code_files:
        assert file.extension
