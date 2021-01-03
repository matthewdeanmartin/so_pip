from so_pip.support_files.setup_py import render_setup_py


def test_render_setup_py():
    model = {
        "package_name": "pn",
        "version": "v",
        "url": "url",
        "author": "au",
        "author_email": "twitter",
        "description": "desc",
        "dependencies": ["a", "b"],
    }

    assert render_setup_py(model)
