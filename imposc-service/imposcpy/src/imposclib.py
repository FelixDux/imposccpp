import pathlib
from libwrapper import LibWrapper


class ImposcIF(LibWrapper):

    def __init__(self):
        libs_path = pathlib.Path(__file__).parent.parent.parent.absolute() / "imposc-cpp/libs"
        super().__init__("imposc_library", "imposcpy", libs_path, libs_path / "imposcpy.h")

    def impacts(self, **kwargs) -> bool:
        return self.make_call("impacts", kwargs)

    def singularity_set(self, **kwargs) -> bool:
        return self.make_call("singularity_set", kwargs)

    def doa(self, **kwargs) -> bool:
        return self.make_call("doa", kwargs)


if __name__ == "__main__":

    imposc = ImposcIF()

    import imposc_library

    outfile = b"myfile.png"
    errorfile = b"errorfile.txt"

    print(dir(imposc_library))

    # if imposc_library.impacts(omega=2.8,r= 0.8, sigma=0, max_periods=100, phi=0.5, v=0.5, num_iterations=20000, outfile=outfile, logfile=errorfile):
    if imposc_library.doa(omega=5.2,r= 0.8, sigma=-0.63, max_periods=100, max_velocity=4, n_v_increments = 200, n_phi_increments=200, n_iterations=800, outfile=outfile, logfile=errorfile):
        from PIL import Image
        im = Image.open(outfile)
        im.show()
    else:
        print(pathlib.Path(errorfile).read_text())