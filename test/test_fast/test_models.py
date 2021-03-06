from so_pip.models.code_block_model import CodeBlock
from so_pip.models.code_file_model import CodeFile
from so_pip.models.python_package_model import CodePackage


def test_code_block():
    # One chunk of code and maybe stuff above and below
    block = CodeBlock()
    block.header_comments = "I will write an example"
    block.raw_text = "print hello, but html style"
    block.code_text = "print('hello world')"
    block.footer_comments = "I wrote that."
    tags = ["python"]
    block.analyze(tags=tags)


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
    psm = CodePackage("name", "desc")
    # how to make an post/question?
    # psm.extract_metadata()
