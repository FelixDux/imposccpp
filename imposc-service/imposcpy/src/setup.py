from distutils.core import setup
from distutils.cmd import Command
from distutils.ccompiler import new_compiler 
from distutils.extension import Extension 
from sysconfig import get_paths 
from Cython.Build import cythonize
from pathlib import Path
from subprocess import run

libs_path = Path(__file__).absolute().parent.parent.parent / "imposc-cpp/libs"
libs_path_str = str(libs_path)

this_dir = Path(__file__).parent.absolute()
package_module = this_dir / "imposc_library"
package_pyx_file = package_module.with_suffix(".pyx")
package_cpp_file = package_module.with_suffix(".cpp")

# TODO: now encountering this issue in Docker https://stackoverflow.com/questions/492374/g-in-what-order-should-static-and-dynamic-libraries-be-linked/492498#492498

imposc_extension = Extension(
    name="imposc_library",
    sources=["imposc_library.pyx"],
    libraries=["stdc++fs"],
    # library_dirs=[libs_path_str],
    # include_dirs=[libs_path_str],
    extra_compile_args = ["-std=c++17"]
)

setup(
    name="imposc_library",
    ext_modules=cythonize([imposc_extension])
    )