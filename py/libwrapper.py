import ctypes
import pathlib
from subprocess import Popen, PIPE
from typing import get_type_hints, Dict, List, Tuple


def wrap_string(s: str):
    return ctypes.create_string_buffer(s.encode('utf-8'))

def wrap_path(path: pathlib.Path):
    return wrap_string(str(path))

def wrap_var(var, type_name: str):
    pass


class LibWrapper:
    _converters = dict([
        ("bool", (ctypes.c_bool, ctypes.c_bool)),
        ("float", (ctypes.c_float, ctypes.c_float)),
        ("double", (ctypes.c_double, ctypes.c_double)),
        ("int", (ctypes.c_int, ctypes.c_int)),
        ("uint", (ctypes.c_uint, ctypes.c_uint)),
        ("Path", (wrap_path, ctypes.POINTER(ctypes.c_char))),
        ("str", (wrap_string, ctypes.POINTER(ctypes.c_char)))
    ])

    def __init__(self, library):
        # Load the shared library into ctypes
        self._libname = str(library)
        self._c_lib = ctypes.CDLL(self._libname)

        self._functions = dict()
        self._parameters = dict()

    def symbol(self, name: str) -> str:
        proc_nm = Popen(["nm", "-D", self._libname], stdout = PIPE)
        proc_grep = Popen(["grep", name], stdin=proc_nm.stdout, stdout=PIPE)
        return proc_grep.communicate()[0].split()[-1].decode()

    def add_function(self, name: str, restype: str, parameters: List[Tuple]):
        symbol = self.symbol(name)
        self._functions[name] = getattr(self._c_lib, symbol)
        self._functions[name].restype = self._converters[restype][1]
        self._functions[name].argtypes = list(map(lambda p: self._converters[p[1]][1], parameters))

        self._parameters[name] = list(map(lambda p: (p[0], self._converters[p[1]]), parameters))

    def make_call(self, function_name: str, args: Dict):
        good_args = list([converter[0](args[key]) for key, converter in self._parameters[function_name] if key in args])

        return self._functions[function_name](*good_args)
