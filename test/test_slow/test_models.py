from so_pip.api_clients.stackapi_facade import get_json_by_question_id, \
    get_json_by_answer_id
from so_pip.models.python_package_model import PythonPackage


def test_handle_metadata_question():
    value = get_json_by_question_id(24139250)["items"][0]
    submodule = PythonPackage(package_name="foo",
                              description="bar")
    submodule.extract_metadata(value)

def test_handle_metadata_answer():
    answer = get_json_by_answer_id(24139629)["items"][0]
    submodule = PythonPackage(package_name="foo",
                              description="bar")
    submodule.extract_metadata(answer)
