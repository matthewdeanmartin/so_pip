from so_pip.parse_code.arbitrary_code_block import find_code_blocks

def test_find_code_blocks_question_text_only():
    result = find_code_blocks(
        "Just tell me the answer"
    )
    assert result
    assert result[0].header_comments

def test_find_code_blocks():
    result = find_code_blocks(
        "<pre><code>\n"
        "def run():\n"
        "   print('hello world')\n"
        "</code></pre>\n"
    )
    assert result
    assert len(result)==1
    assert result[0].is_valid_python
    assert "hello" in result[0].code_text
    assert not result[0].header_comments
    assert not result[0].footer_comments
    assert result[0].extension ==".py"

def test_find_code_blocks_with_header():
    result = find_code_blocks(
        "What is this thing"
        "<pre><code>\n"
        "def run():\n"
        "   print('hello world')\n"
        "</code></pre>\n"
    )
    assert result
    assert len(result)==1
    assert result[0].is_valid_python
    assert "hello" in result[0].code_text
    assert result[0].header_comments
    assert not result[0].footer_comments
    assert result[0].extension ==".py"

def test_find_code_blocks_with_header_and_footer():
    result = find_code_blocks(
        "What is this thing"
        "<pre><code>\n"
        "def run():\n"
        "   print('hello world')\n"
        "</code></pre>"
        "so a footer\n"
    )
    assert result
    assert len(result)==1
    assert result[0].is_valid_python
    assert "hello" in result[0].code_text
    assert result[0].header_comments
    assert result[0].footer_comments
    assert result[0].extension ==".py"
