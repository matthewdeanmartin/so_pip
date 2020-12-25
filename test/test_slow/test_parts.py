from so_pip.api_clients.pystackexchange_facade import question_by_id
from so_pip.parse_python.module_maker import handle_python_post


def test_handle_python_answer():
    value = question_by_id(24139250)

    answer = value.answers[0]
    submodule = handle_python_post(
            answer.body, "answer_module_name", f"StackOverflow answer #{answer.id}"
        )
    assert submodule.code_blocks
    assert submodule.code_files
    assert sum(len(file.code_blocks) for file in submodule.code_files)==len(submodule.code_blocks)
    for file in submodule.code_files:
        assert file.extension
