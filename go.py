from setuptools_scm import get_version
from setuptools_scm.version import guess_next_version


def version_scheme(version):
    verstr = str(version.tag)
    ver = verstr.split(".")
    return "{}.{}.{}".format(ver[0], ver[1], int(ver[2]) + 1)


v = get_version(
    version_scheme=version_scheme,
    local_scheme=lambda *args, **kwargs: "",
)
print(guess_next_version(v))
