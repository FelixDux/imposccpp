from image_cache import ImageCache
from imposclib import ImposcIF
from pathlib import Path
from PIL import Image

class ImposcActions:

    def __init__(self):
        self._cache = ImageCache()
        self._imposclib = ImposcIF(self._cache.cache_path)

    def impacts(self, omega: float, r: float, sigma: float, max_periods: int, phi: float, v: float, num_iterations: int):
        outfile = self._cache.offer_new_file()
        if self._imposclib.impacts(omega, r, sigma, max_periods, phi, v, num_iterations, outfile):
            return outfile
        else:
            return Path()

    def singularity_set(self, omega: float, r: float, sigma: float, max_periods: int, num_points: int):
        outfile = self._cache.offer_new_file()
        if self._imposclib.singularity_set(omega, r, sigma, max_periods, num_points, outfile):
            return outfile
        else:
            return Path()

    def doa(self, omega: float, r: float, sigma: float, max_periods: int, max_velocity: float, n_v_increments: int, n_phi_increments: int):
        outfile = self._cache.offer_new_file()
        if self._imposclib.doa(omega, r, sigma, max_periods, max_velocity, n_v_increments, n_phi_increments, outfile):
            return outfile
        else:
            return Path()

def do_and_show(image_file):
    if image_file.exists():
        Image.open(image_file).show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Impact oscillator plots')
    parser.add_argument("-p", "--plot", help="Type of plot", choices=['scatter', 'singularity-set', 'doa'], required=True)
    parser.add_argument("-o", "--omega", type=float, help="The forcing frequency", required=True)
    parser.add_argument("-r", "--r", type=float, help="The coefficient of restitution", required=True)
    parser.add_argument("-s", "--sigma", type=float, help="The obstacle offset", required=True)
    parser.add_argument("-n", "--max-periods", default=100, type=int, help="The number of forcing cycles before the simulator will assume that an impact will not succeed")
    parser.add_argument("-f", "--phi", type=float, help="The initial phase", default=0.5)
    parser.add_argument("-v", "--v", type=float, help="The initial velocity", default=0.0)
    parser.add_argument("-m", "--max-velocity", type=float, help="The initial velocity", default=0.0)
    parser.add_argument("-i", "--num-impacts", default=1000, type=int, help="The number of impacts")
    parser.add_argument("--n-v-increments", default=400, type=int, help="The number of v increments for a doa plot")
    parser.add_argument("--n-phi-increments", default=400, type=int, help="The number of phase increments for a doa plot")

    args = parser.parse_args()

    actions = ImposcActions()

    if args.plot == "scatter":
        do_and_show(actions.impacts(args.omega, args.r, args.sigma, args.max_periods, args.phi, args.v, args.num_impacts))

    if args.plot == "singularity-set":
        do_and_show(actions.singularity_set(args.omega, args.r, args.sigma, args.max_periods, args.num_iterations))

    if args.plot == "doa":
        do_and_show(actions.doa(args.omega, args.r, args.sigma, args.max_periods, args.max_velocity, args.n_v_increments, args.n_phi_increments))


