import pathlib
from libwrapper import LibWrapper, wrap_path


class ImposcIF(LibWrapper):

    def __init__(self):
        super().__init__(pathlib.Path(__file__).parent.parent.absolute() / "build/imposcpy/libimposcpy.so")

        self.add_function("map_impacts", "bool", 
            [("omega", "double"), ("r", "double"), ("sigma", "double"), ("max_periods", "uint"), ("phi", "double"), ("v", "double"), ("num_iterations", "uint"), ("outfile", "Path")]
            )
        self.add_function("map_singularity_set", "bool", 
            [("omega", "double"), ("r", "double"), ("sigma", "double"), ("max_periods", "uint"), ("num_points", "uint"), ("outfile", "Path")]
            )
        self.add_function("map_doa", "bool", 
            [("omega", "double"), ("r", "double"), ("sigma", "double"), ("max_periods", "uint"), ("max_velocity", "double"), ("n_v_increments", "uint"), ("n_phi_increments", "uint"), ("outfile", "Path")]
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

    print(imposc.impacts(omega=5.2,r= 0.8, sigma=0, max_periods=100, phi=0.5, v=0.5, num_iterations=1000, outfile=outfile))