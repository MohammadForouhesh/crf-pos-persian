import sys
import distutils.util
from setuptools import setup, find_packages
from pathlib import Path

PACKAGES = find_packages()
COMPILE_OPTIONS = {
    "msvc": ["/Ox", "/EHsc"],
    "other": ["-O3", "-Wno-strict-prototypes", "-Wno-unused-function"],
}
COMPILER_DIRECTIVES = {
    "language_level": -3,
    "embedsignature": True,
    "annotation_typing": False,
}
LINK_OPTIONS = {"msvc": [], "other": []}


def is_new_osx():
    """Check whether we're on OSX >= 10.10"""
    name = distutils.util.get_platform()
    if sys.platform != "darwin":
        return False
    elif name.startswith("macosx-10"):
        minor_version = int(name.split("-")[1].split(".")[1])
        if minor_version >= 7:
            return True
        else:
            return False
    else:
        return False


if is_new_osx():
    COMPILE_OPTIONS["other"].append("-stdlib=libc++")
    LINK_OPTIONS["other"].append("-lc++")
    LINK_OPTIONS["other"].append("-nodefaultlibs")


def clean(path):
    for path in path.glob("**/*"):
        if path.is_file() and path.suffix in (".so", ".cpp"):
            print(f"Deleting {path.name}")
            path.unlink()


def setup_package():
    root = Path(__file__).parent

    setup(
        name='crf_pos',
        packages=PACKAGES,
        version='2.0.0',
        url='https://github.com/MohammadForouhesh/crf-pos-persian',
        license='MIT',
        author='MohammadForouhesh',
        author_email='Mohammadh.Forouhesh@gmail.com',
        description='Persian Part-of-Speech tagger framework',
        package_data={"": ["*.pyx", "*.pxd", "*.pxi", "*.cu"]},
    )


if __name__ == '__main__':
    setup_package()
