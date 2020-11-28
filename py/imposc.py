import ctypes
import pathlib
from subprocess import Popen, PIPE


def wrap_string(s: str):
    return ctypes.create_string_buffer(s.encode('utf-8'))

class ImposcIF:

    # using nm -D libimposcpy.so to get symbols

    def __init__(self, images: pathlib.Path):
        # Load the shared library into ctypes
        self.libname = pathlib.Path(__file__).parent.parent.absolute() / "build/imposcpy/libimposcpy.so"
        self.c_lib = ctypes.CDLL(self.libname)

        self.functions = dict()

        self.add_function("map_impacts")
        self.add_function("map_singularity_set")
        self.add_function("map_doa")

        self.images = images.absolute()

    def symbol(self, name: str) -> str:
        proc_nm = Popen(["nm", "-D", self.libname], stdout = PIPE)
        proc_grep = Popen(["grep", name], stdin=proc_nm.stdout, stdout=PIPE)
        return proc_grep.communicate()[0].split()[2].decode()

    def add_function(self, name: str):
        self.functions[name] = getattr(self.c_lib, self.symbol(name))
        self.functions[name].restype = ctypes.c_bool

    def image_file(self, outfile: str):
        return wrap_string(str(self.images / outfile))

    def impacts(self, omega: float, r: float, sigma: float, max_periods: int, phi: float, v: float, num_iterations: int, outfile: str) -> bool:
        return self.functions["map_impacts"](ctypes.c_double(omega), ctypes.c_double(r), ctypes.c_double(sigma), ctypes.c_uint(max_periods),
                ctypes.c_double(phi), ctypes.c_double(v), ctypes.c_uint(num_iterations), self.image_file(outfile))

    def singularity_set(self, omega: float, r: float, sigma: float, max_periods: int, num_points: int, outfile: str) -> bool:
        return self.functions["map_singularity_set"](ctypes.c_double(omega), ctypes.c_double(r), ctypes.c_double(sigma), ctypes.c_uint(max_periods),
                ctypes.c_uint(num_points), self.image_file(outfile))

    def doa(self, omega: float, r: float, sigma: float, max_periods: int, max_velocity: float, n_v_increments: int, n_phi_increments: int, outfile: str) -> bool:
        return self.functions["map_doa"](ctypes.c_double(omega), ctypes.c_double(sigma), ctypes.c_uint(max_periods),
                ctypes.c_double(max_velocity), ctypes.c_uint(n_v_increments), ctypes.c_uint(n_phi_increments), self.image_file(outfile))


if __name__ == "__main__":

    imposc = ImposcIF(pathlib.Path(__file__).parent)

    imposc.impacts(2.8, 0.8, 0, 100, 0.5, 0.5, 1000, "myfile.png")