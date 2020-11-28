import ctypes
import pathlib


def wrap_string(s: str):
    return ctypes.create_string_buffer(s.encode('utf-8'))

class ImposcIF:

    # using nm -D libimposcpy.so to get symbols

    def __init__(self, images: pathlib.Path):
        # Load the shared library into ctypes
        libname = pathlib.Path(__file__).parent.parent.absolute() / "build/imposcpy/libimposcpy.so"
        self.c_lib = ctypes.CDLL(libname)

        self.c_lib._Z11map_impactsdddjddjPKc.restype = ctypes.c_bool
        self.c_lib._Z19map_singularity_setdddjjPKc.restype = ctypes.c_bool
        self.c_lib._Z7map_doadddjdjjjPKc.restype = ctypes.c_bool

        self.images = images.absolute()

    def image_file(self, outfile: str):
        return wrap_string(str(self.images / outfile))

    def impacts(self, omega: float, r: float, sigma: float, max_periods: int, phi: float, v: float, num_iterations: int, outfile: str) -> bool:
        return self.c_lib._Z11map_impactsdddjddjPKc(ctypes.c_double(omega), ctypes.c_double(r), ctypes.c_double(sigma), ctypes.c_uint(max_periods),
                ctypes.c_double(phi), ctypes.c_double(v), ctypes.c_uint(num_iterations), self.image_file(outfile))

    def singularity_set(self, omega: float, r: float, sigma: float, max_periods: int, num_points: int, outfile: str) -> bool:
        return self.c_lib._Z19map_singularity_setdddjjPKc(ctypes.c_double(omega), ctypes.c_double(r), ctypes.c_double(sigma), ctypes.c_uint(max_periods),
                ctypes.c_uint(num_points), self.image_file(outfile))

    def doa(self, omega: float, r: float, sigma: float, max_periods: int, max_velocity: float, n_v_increments: int, n_phi_increments: int, outfile: str) -> bool:
        return self.c_lib._Z7map_doadddjdjjjPKc(ctypes.c_double(omega), ctypes.c_double(sigma), ctypes.c_uint(max_periods),
                ctypes.c_double(max_velocity), ctypes.c_uint(n_v_increments), ctypes.c_uint(n_phi_increments), self.image_file(outfile))


if __name__ == "__main__":

    imposc = ImposcIF(pathlib.Path(__file__).parent)

    imposc.impacts(5.2, 0.8, 0, 100, 0.5, 0.5, 1000, "myfile.png")