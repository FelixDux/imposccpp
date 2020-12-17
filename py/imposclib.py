import pathlib
from libwrapper import LibWrapper, wrap_path


class ImposcIF(LibWrapper):

    def __init__(self):
        super().__init__(pathlib.Path(__file__).parent.parent.absolute() / "build/imposcpy/libimposcpy.so")

        self.add_function("map_impacts", "bool", 
            [("omega", "double"), ("r", "double"), ("sigma", "double"), ("max_periods", "uint"), ("phi", "double"), ("v", "double"), ("num_impacts", "uint"), ("outfile", "Path"), ("errorfile", "Path")]
            )
        self.add_function("map_singularity_set", "bool", 
            [("omega", "double"), ("r", "double"), ("sigma", "double"), ("max_periods", "uint"), ("num_points", "uint"), ("outfile", "Path"), ("errorfile", "Path")]
            )
        self.add_function("map_doa", "bool", 
            [("omega", "double"), ("r", "double"), ("sigma", "double"), ("max_periods", "uint"), ("max_velocity", "double"), ("n_v_increments", "uint"), ("n_phi_increments", "uint"), ("outfile", "Path"), ("errorfile", "Path")]
            )

    def impacts(self, **kwargs) -> bool:
        return self.make_call("map_impacts", kwargs)

    def singularity_set(self, **kwargs) -> bool:
        return self.make_call("map_singularity_set", kwargs)

    def doa(self, **kwargs) -> bool:
        return self.make_call("map_doa", kwargs)


if __name__ == "__main__":

    imposc = ImposcIF()

    # outfile = str(pathlib.Path(__file__).parent.absolute() /  "myfile.png")
    outfile = "myfile.png"
    errorfile = "errorfile.txt"

    if imposc.impacts(omega=2.8,r= 0.8, sigma=0, max_periods=100, phi=0.5, v=0.5, num_impacts=1000, outfile=outfile, errorfile=errorfile):
        from PIL import Image
        im = Image.open(outfile)
        im.show()
    else:
        print(pathlib.Path(errorfile).read_text())