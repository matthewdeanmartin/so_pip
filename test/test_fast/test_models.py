from so_pip.models.model import CodeBlock, PythonPackage, CodeFile


def test_code_block():
    # One chunk of code and maybe stuff above and below
    block = CodeBlock()
    block.header_comments = "I will write an example"
    block.raw_text = "print hello, but html style"
    block.code_text = "print('hello world')"
    block.footer_comments = "I wrote that."
    block.analyze()

def test_code_file_single_block():
    # Maybe many chunks of code.
    file = CodeFile()
    file.file_name = "foo.py"
    block = CodeBlock()
    block.header_comments = "I will write an example"
    block.raw_text = "print hello, but html style"
    block.code_text = "print('hello world')"
    file.code_blocks.append(block)
    file.to_write()
    file.all_code()

def test_code_file_two_blocks():
    # Maybe many chunks of code.
    file = CodeFile()
    file.file_name = "foo.py"
    block = CodeBlock()
    block.header_comments = "I will write an example"
    block.raw_text = "print hello, but html style"
    block.code_text = "print('hello world')"
    file.code_blocks.append(block)

    block = CodeBlock()
    block.header_comments = "Now for some more"
    block.raw_text = "print hello, but html style"
    block.code_text = "print('goodbye world')"
    file.code_blocks.append(block)
    file.to_write()
    file.all_code()
    assert file.non_comment_lines()
    assert file.all_code()
    assert file.to_write()

def test_python_submodule():
    psm = PythonPackage("name", "desc")
    # how to make an answer/question?
    # psm.extract_metadata()
