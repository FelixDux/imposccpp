from image_cache import ImageCache
from imposclib import ImposcIF
from pathlib import Path
from PIL import Image
from lib_errors import LibErrors


class ImposcActions:

    def __init__(self):
        self._cache = ImageCache()
        self._imposclib = ImposcIF()

    def impacts(self, **kwargs) -> Path:
        errors = LibErrors()
        outfile = self._cache.offer_new_file()
        if self._imposclib.impacts(outfile=outfile, errorfile=errors.errorFile, **kwargs):
            return outfile
        else:
            return errors.errorPath

    def singularity_set(self, **kwargs) -> Path:
        errors = LibErrors()
        outfile = self._cache.offer_new_file()
        if self._imposclib.singularity_set(outfile=outfile, errorfile=errors.errorFile, **kwargs):
            return outfile
        else:
            return errors.errorPath

    def doa(self, **kwargs) -> Path:
        errors = LibErrors()
        outfile = self._cache.offer_new_file()
        if self._imposclib.doa(outfile=outfile, errorfile=errors.errorFile, **kwargs):
            return outfile
        else:
            return errors.errorPath
            

def do_and_show(image_file):
    if image_file.exists():
        if image_file.suffix == ".txt":
            print(image_file.read_text())
        else:
            Image.open(image_file).show()
        

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Impact oscillator plots')
    parser.add_argument("-p", "--plot", help="Type of plot", choices=['impacts', 'singularity-set', 'doa'], required=True)
    parser.add_argument("-o", "--omega", type=float, help="The forcing frequency", required=True)
    parser.add_argument("-r", "--r", type=float, help="The coefficient of restitution", required=True)
    parser.add_argument("-s", "--sigma", type=float, help="The obstacle offset", required=True)
    parser.add_argument("-n", "--max-periods", default=100, type=int, help="The number of forcing cycles before the simulator will assume that an impact will not succeed")
    parser.add_argument("-f", "--phi", type=float, help="The initial phase", default=0.5)
    parser.add_argument("-v", "--v", type=float, help="The initial velocity", default=0.0)
    parser.add_argument("-m", "--max-velocity", type=float, help="The initial velocity", default=0.0)
    parser.add_argument("-i", "--num-impacts", default=4000, type=int, help="The number of impacts")
    parser.add_argument("--n-v-increments", default=100, type=int, help="The number of v increments for a doa plot")
    parser.add_argument("--n-phi-increments", default=100, type=int, help="The number of phase increments for a doa plot")

    args = vars(parser.parse_args())

    actions = ImposcActions()

    if args.pop('plot') == "impacts":
        do_and_show(actions.impacts(**args))

    elif args.pop('plot') == "singularity-set":
        do_and_show(actions.singularity_set(**args))

    elif args.pop('plot') == "doa":
        do_and_show(actions.doa(**args))

