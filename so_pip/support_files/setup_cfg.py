"""
Create ini file for setup.py.

The setup.cfg file is weird. It can only override values in setup.py
and is used by some tools as a centralized config.ini file.
"""
def create_setup_cfg() -> None:
    """[metadata]
    name = some_name
    version = attr: some_package.VERSION
    description = Some description
    long_description = file: README
    keywords = one, two
    license = BSD 3-Clause License"""
    raise NotImplementedError()
