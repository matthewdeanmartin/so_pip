"""
Wrap in run or class
"""


def wrap_in_run(code: str) -> str:
    """Probably a miracle if this works for everything"""
    code = code.strip("\n ")
    imports = []
    lines = []
    dropped_def_run = False
    # first pass

    last_was_import = False
    run_comment = '    """"Run script"""'
    for line in code.split("\n"):
        if "import" in line.split():
            last_was_import = True
            imports.append(line)
            continue
        if line.isspace() and last_was_import:
            imports.append(line)
            continue
        if not dropped_def_run:
            if len(imports+lines) > 0 and not (imports+lines)[-1].isspace():
                lines.append("")
            lines.append("def run() -> None:")
            lines.append(run_comment)
            dropped_def_run = True
            continue
        # reduce whitespace around def run
        if line.isspace() or not line:
            if len(lines) > 0 and not lines[-1] == run_comment:
                lines.append(line)
                continue
            else:
                continue
        else:
            # non whitepspace
            if dropped_def_run:
                lines.append("     " + line)
                continue
            lines.append(line)

    if len(imports+lines) > 0 and not (imports+lines)[-1].isspace():
        lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append("     run()")
    return "\n".join(imports + lines)


if __name__ == '__main__':
    result = wrap_in_run("""import foo
import bar

from baz import blerg

print("hello world")

""")
    print(result)
