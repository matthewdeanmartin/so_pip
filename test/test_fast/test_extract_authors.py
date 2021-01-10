from so_pip.models.authors_model import email_from_bio


def test_email_from_bio():
    results = email_from_bio("my email addresses are foo@gmail.com and bar@yahoo.com")
    assert "foo@gmail.com" in results
    assert "bar@yahoo.com" in results
    assert len(results) == 2
