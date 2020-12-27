import pathlib
from libwrapper import LibWrapper, wrap_path


class ImposcIF(LibWrapper):

    def __init__(self):
        super().__init__(pathlib.Path(__file__).parent.parent.absolute() / "imposc-cpp/build/imposcpy/libimposcpy.so")

    def impacts(self, **kwargs) -> bool:
        return self.make_call("map_impacts", kwargs)

    def singularity_set(self, **kwargs) -> bool:
        return self.make_call("map_singularity_set", kwargs)

    def doa(self, **kwargs) -> bool:
        return self.make_call("map_doa", kwargs)


if __name__ == "__main__":

    imposc = ImposcIF()

    outfile = "myfile.png"
    errorfile = "errorfile.txt"

    if imposc.impacts(omega=2.8,r= 0.8, sigma=0, max_periods=100, phi=0.5, v=0.5, num_impacts=1000, outfile=outfile, errorfile=errorfile):
        from PIL import Image
        im = Image.open(outfile)
        im.show()
    else:
        print(pathlib.Path(errorfile).read_text())