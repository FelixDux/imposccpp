from pathlib import Path
from typing import get_type_hints, Dict, List, Tuple
import importlib
from os import getcwd, environ, getenv
from shutil import move, copy
from subprocess import run


def build_wrapper(package_name: str, library_name: str, library_dir: Path, header_file: Path):
    """ Builds the package if it is not already present and then imports it """

    this_dir = Path(__file__).parent.absolute()
    package_module = this_dir / f"{package_name}"

    package_extension = run(["python3.8-config", "--extension-suffix"], capture_output=True).stdout.decode().strip()

    package_library_file = Path(f"{package_module}{package_extension}")

    if not package_library_file.is_file() or True:
        package_pyx_file = package_module.with_suffix(".pyx")
        package_cpp_file = package_module.with_suffix(".cpp")

        lib_files = library_dir.glob("lib*.so")
        libs = []

        for f in lib_files:
            libs.append(f.name) 
            copy(str(f), str(this_dir / f.name))

        lib_names = ' '.join([f.split('.')[0].replace('lib','-l') for f in libs])

        cython_command = f"cython --working {this_dir} --cplus -I {library_dir} -3 {package_pyx_file} -o {package_cpp_file}".split(' ')
        
        run(cython_command)

        c_flags = "-I/usr/include/python3.8 -Wno-unused-result -Wsign-compare -g -fdebug-prefix-map=/build/python3.8-xhc1jt/python3.8-3.8.5=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector -Wformat -Werror=format-security -DNDEBUG -g -fwrapv -O3 -Wall" #run(["python3.8-config", "--cflags"], capture_output=True).stdout.decode().strip()
        
        ld_flags = run(["python3.8-config", "--ldflags"], capture_output=True).stdout.decode().strip()

        build_command = f"g++ {c_flags} -shared -fPIC -std=c++17 -I{library_dir} {package_cpp_file} -o {package_library_file} {ld_flags} -L{this_dir} {lib_names} -Wl,-rpath,{this_dir} -Wl,-R -Wl,{this_dir}"
        
        build_tokens = [t for t in build_command.split(' ') if t]
        
        run(build_tokens)

    return importlib.import_module(package_name)


class LibWrapper:
    def __init__(self, package_name: str, library_name: str, library_dir: Path, header_file: Path):

        # self._libname = str(library)
        self._c_lib = build_wrapper(package_name, library_name, library_dir, header_file)

        self._functions = dict()
        self._parameters = dict()

    def add_function(self, name: str, restype: str, parameters: List[Tuple]):
        
        self._functions[name] = getattr(self._c_lib, name)

        self._parameters[name] = list(map(lambda p: (p[0], p[1]), parameters))

    def make_call(self, function_name: str, args: Dict):
        good_args = list([args[param[0]] for param in self._parameters[function_name] if param[0] in args])
        print(args)

        print(good_args)

        return self._functions[function_name](*good_args)
