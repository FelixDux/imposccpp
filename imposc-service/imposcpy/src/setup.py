from distutils.core import setup
from distutils.cmd import Command
from distutils.ccompiler import new_compiler 
from distutils.extension import Extension 
from sysconfig import get_paths 
from Cython.Build import cythonize
from pathlib import Path
from subprocess import run, Popen, PIPE
from os import environ

# We need to make sure we use gcc, not clang - on a make gcc is just and alias for clang
def get_gcc(start_version):
    if start_version <= 0:
        return

    gcc = [f"gcc-{start_version}", f"g++-{start_version}"]
    cc = ["CC","CXX"]

    do_shell = lambda x: Popen(["which", x], stdout=PIPE, stderr=PIPE).communicate()[0].decode("utf-8")

    def setenv(c, g):
        environ[c] = g
    
    gs = list(map(do_shell, gcc))

    if (all(gs)):
        for c, g in zip(cc, gs):
            setenv(c, g)
    else:
        get_gcc(start_version-1)
    

get_gcc(12)

libs_path = Path(__file__).absolute().parent.parent.parent / "imposc-cpp/libs"
libs_path_str = str(libs_path)

this_dir = Path(__file__).parent.absolute()
package_module = this_dir / "imposc_library"
package_pyx_file = package_module.with_suffix(".pyx")
package_cpp_file = package_module.with_suffix(".cpp")

# The libraries argument is needed to avoid an issue with link order -
# see https://stackoverflow.com/questions/492374/g-in-what-order-should-static-and-dynamic-libraries-be-linked/492498#492498
imposc_extension = Extension(
    name="imposc_library",
    sources=["imposc_library.pyx"],
    libraries=["stdc++fs"],
    extra_compile_args = ["-std=c++17"]
)

setup(
    name="imposc_library",
    ext_modules=cythonize([imposc_extension])
    )