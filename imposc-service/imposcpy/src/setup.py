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

# static_libs = libs_path.glob("libimposcpy.a")

# this_dir = Path(__file__).parent.absolute()
# package_module = this_dir / "imposc_library"
# package_pyx_file = package_module.with_suffix(".pyx")
# package_cpp_file = package_module.with_suffix(".cpp")

# class imposc_static(Command): 
#     description = 'build static lib' 
#     user_options = [] # do not remove, needs to be stubbed out! 
#     python_info = get_paths() 

#     def initialize_options(self):
#         pass

#     def finalize_options(self):
#         pass

#     def run(self):

#         cython_command = f"cython --working . --cplus -I {libs_path_str} -3 {package_pyx_file} -o {package_cpp_file}".split(' ')
        
#         run(cython_command)

#         # Create compiler with default options
#         c = new_compiler()

#         c.add_include_dir(libs_path_str)

#         c.add_include_dir(self.python_info['include'])
#         # Compile into .o files
#         objects = c.compile([str(package_cpp_file)])

#         # Create static or shared library
#         c.create_static_lib(list([str(lib) for lib in static_libs]), "imposc_library", output_dir=".")

# setup(
#     name="imposc_library",
#     cmdclass={'imposc_static': imposc_static}
#     )

imposc_extension = Extension(
    name="imposc_library",
    sources=["imposc_library.pyx"],
    # libraries=["imposcpy"],
    # library_dirs=[libs_path_str],
    # include_dirs=[libs_path_str],
    extra_compile_args = ["-std=c++17"],
    # extra_objects=list([str(lib) for lib in static_libs])
)

setup(
    name="imposc_library",
    ext_modules=cythonize([imposc_extension])
    )