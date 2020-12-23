# !/usr/bin/env python
import codecs
import os
from setuptools import find_packages
from distutils.core import setup


PROJECT_NAME = "so_pip"

here = os.path.abspath(os.path.dirname(__file__))
#with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
#long_description = f.read()
#    print(long_description)
#long_description = long_description.replace("\n\n", "\n").replace("\r\n", "\n")
long_description = "Generate module code from a stackoverflow answer"
about = {}
with open(os.path.join(here, PROJECT_NAME, "_version.py")) as f:
    exec(f.read(), about)

required = [

]

description = "Formalizing copy-paste from StackOverflow"
setup(
    name=PROJECT_NAME,
    version=about["__version__"],
    description=description,
    long_description=long_description,
    # markdown is not supported. Easier to just convert md to rst with pandoc
    long_description_content_type="text/x-rst",
    author="Matthew Martin",
    author_email="matthewdeanmartin@gmail.com",
    url="https://github.com/matthewdeanmartin/" + PROJECT_NAME,
    packages=find_packages(exclude=["test"]),
    entry_points={
        "console_scripts": ["so_pip=so_pip.__main__:process_docopts"]
    },
    install_requires=required,
    extras_require={},
    include_package_data=True,
    license="MIT",
    keywords="stackoverflow",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    cmdclass={},
    setup_requires=[],
)
