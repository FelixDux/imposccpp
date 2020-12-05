import ctypes
import pathlib
from subprocess import Popen, PIPE


def wrap_string(s: str):
    return ctypes.create_string_buffer(s.encode('utf-8'))

def wrap_path(path: pathlib.Path):
    return wrap_string(str(path))

class ImposcIF:

    # using nm -D libimposcpy.so to get symbols

    def __init__(self):
        # Load the shared library into ctypes
        self._libname = pathlib.Path(__file__).parent.parent.absolute() / "build/imposcpy/libimposcpy.so"
        self._c_lib = ctypes.CDLL(self._libname)

        self._functions = dict()

        self.add_function("map_impacts")
        self.add_function("map_singularity_set")
        self.add_function("map_doa")

    def symbol(self, name: str) -> str:
        proc_nm = Popen(["nm", "-D", self._libname], stdout = PIPE)
        proc_grep = Popen(["grep", name], stdin=proc_nm.stdout, stdout=PIPE)
        return proc_grep.communicate()[0].split()[2].decode()

    def add_function(self, name: str):
        self._functions[name] = getattr(self._c_lib, self.symbol(name))
        self._functions[name].restype = ctypes.c_bool

    def impacts(self, omega: float, r: float, sigma: float, max_periods: int, phi: float, v: float, num_iterations: int, outfile: pathlib.Path) -> bool:
        return self._functions["map_impacts"](ctypes.c_double(omega), 
            ctypes.c_double(r), 
            ctypes.c_double(sigma), 
            ctypes.c_uint(max_periods),
                ctypes.c_double(phi), ctypes.c_double(v), ctypes.c_uint(num_iterations), wrap_path(outfile))

    def singularity_set(self, omega: float, r: float, sigma: float, max_periods: int, num_points: int, outfile: pathlib.Path) -> bool:
        return self._functions["map_singularity_set"](ctypes.c_double(omega), ctypes.c_double(r), ctypes.c_double(sigma), ctypes.c_uint(max_periods),
                ctypes.c_uint(num_points), wrap_path(outfile))

    def doa(self, omega: float, r: float, sigma: float, max_periods: int, max_velocity: float, n_v_increments: int, n_phi_increments: int, outfile: pathlib.Path) -> bool:
        return self._functions["map_doa"](ctypes.c_double(omega), ctypes.c_double(sigma), ctypes.c_uint(max_periods),
                ctypes.c_double(max_velocity), ctypes.c_uint(n_v_increments), ctypes.c_uint(n_phi_increments), wrap_path(outfile))


if __name__ == "__main__":

    imposc = ImposcIF()

    # outfile = str(pathlib.Path(__file__).parent.absolute() /  "myfile.png")
    outfile = "myfile.png"

    imposc.impacts(2.8, 0.8, 0, 100, 0.5, 0.5, 1000, outfile)