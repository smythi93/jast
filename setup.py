import sys
import os
import platform
import fnmatch
import setuptools

target = platform.system().lower()
PLATFORMS = {"windows", "linux", "darwin", "cygwin"}
for known in PLATFORMS:
    if target.startswith(known):
        target = known


def run_setup(with_binary):
    if with_binary:
        extra_compile_args = {
            "windows": ["/DANTLR4CPP_STATIC", "/Zc:__cplusplus", "/std:c++17"],
            "linux": ["-std=c++17"],
            "darwin": ["-std=c++17"],
            "cygwin": ["-std=c++17"],
        }
        parser_ext = setuptools.Extension(
            name="jast._parser.sa_java_cpp_parser",
            include_dirs=[os.path.join("_cpp_parser", "antlr4_cpp_runtime")],
            sources=get_files("_cpp_parser", "*.cpp"),
            depends=get_files("_cpp_parser", "*.h"),
            extra_compile_args=extra_compile_args.get(target, []),
        )
        ext_modules = [parser_ext]
    else:
        ext_modules = []

    # Define a package
    setuptools.setup(
        name="java-ast",
        version="1.0.3",
        description="jAST: Analyzing and Modifying Java ASTs with Python",
        packages=setuptools.find_packages("src"),
        package_dir={"": "src"},
        include_package_data=True,
        ext_modules=ext_modules,
        cmdclass={"build_ext": ve_build_ext},
    )


# ===============================================================================
from setuptools.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError


def get_files(path, pattern):
    """
    Recursive file search that is compatible with python3.4 and older
    """
    matches = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


class BuildFailed(Exception):
    pass


class ve_build_ext(build_ext):
    """
    This class extends setuptools to fail with a common BuildFailed exception
    if a build fails
    """

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError):
            raise BuildFailed()
        except ValueError:
            # this can happen on Windows 64 bit, see Python issue 7511
            if "'path'" in str(sys.exc_info()[1]):  # works with Python 2 and 3
                raise BuildFailed()
            raise


is_jython = "java" in sys.platform
is_pypy = hasattr(sys, "pypy_version_info")
using_fallback = is_jython or is_pypy

if not using_fallback:
    try:
        run_setup(with_binary=True)
    except BuildFailed:
        if "JAST_REQUIRE_CI_BINARY_BUILD" in os.environ:
            raise
        else:
            using_fallback = True

if using_fallback:
    run_setup(with_binary=False)
