from setuptools_scm import get_version
from setuptools_scm.version import guess_next_version

v = get_version()
print(guess_next_version(v))
