from so_pip.api_clients.pystackexchange_facade import question_by_id, answer_by_id
from so_pip.support_files.authors import get_authors_for_question, \
    get_authors_for_answer

def test_authors_with_comments():
    q = question_by_id(55019378)
    authors = get_authors_for_question(q)
    assert authors

def test_authors():
    q = question_by_id(9733638)
    a = answer_by_id(26344315)
    authors = get_authors_for_question(q)
    assert authors
    more_authors = get_authors_for_answer(a)
    assert more_authors
