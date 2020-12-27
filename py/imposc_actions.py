from image_cache import ImageCache
from imposclib import ImposcIF
from pathlib import Path
from PIL import Image
from lib_errors import LibErrors
from dataclasses import dataclass, asdict
from typing import Tuple, List


@dataclass
class ActionParameter:
    group: str
    name: str
    description: str
    range: str
    type: str
    label: str

    def toArg(self) -> Tuple[str, str]:
        return (self.name, self.type)


class ActionParameterCollection:
    def __init__(self):
        self._groups = dict()
        self._parameters = dict()

        self.add(ActionParameter(group="Parameters", name = 'omega', description = 'Forcing frequency', range = 'positive', type = 'double', label = 'ω'))
        self.add(ActionParameter(group="Parameters", name = 'sigma', description = 'Obstacle offset', range = '', type = 'double', label = 'σ'))
        self.add(ActionParameter(group="Parameters", name = 'r', description = 'Coefficient of restitution', range = 'non-negative', type = 'double', label = 'r'))
    
        self.add(ActionParameter(group="Initial", name = 'phi', description = 'Phase (modulo 1)', range = 'circle', type = 'double', label = 'φ'))
        self.add(ActionParameter(group="Initial", name = 'v', description = 'Velocity', range = 'non-negative', type = 'double', label = 'v'))
    
        self.add(ActionParameter(group="Options", name = 'max_periods', description = 'Max forcing periods between impacts', range = 'positive', type = 'uint', label = 'P'))
        self.add(ActionParameter(group="Options", name = 'num_impacts', description = 'Number of impacts to plot', range = 'positive', type = 'uint', label = 'N'))
        self.add(ActionParameter(group="Options", name = 'num_points', description = 'Number points along singularity set', range = 'positive', type = 'uint', label = 'M'))
        self.add(ActionParameter(group="Options", name = 'n_phi_increments', description = 'Number of phase increments for DOA plot', range = 'positive', type = 'uint', label = 'Nφ'))
        self.add(ActionParameter(group="Options", name = 'n_v_increments', description = 'Number of velocity increments for DOA plot', range = 'positive', type = 'uint', label = 'Nv'))
        self.add(ActionParameter(group="Options", name = 'max_velocity', description = 'Maximum velocity for DOA plot', range = 'non-negative', type = 'double', label = 'vmax'))

    def add(self, parameter: ActionParameter) -> None:
        self._parameters[parameter.name] = parameter

        if parameter.group not in self._groups:
            self._groups[parameter.group] = list()

        self._groups[parameter.group].append(dict(filter(lambda item: item[0] !="group", asdict(parameter).items())))

    def args(self, names: List[str]) -> List[Tuple[str,str]]:
        return list(map(lambda name: self._parameters[name].toArg(), filter(lambda name: name in self._parameters, names)))

    def action_info(self, names: List[str]) -> dict:
        info = dict()

        for k, v in self._groups.items():
            info[k] = list(filter(lambda p: p['name'] in names, v))

        return info


class ActionCollection:
    def __init__(self):
        self._parameters = ActionParameterCollection()
        self._actions = dict([
            ('impacts', ["omega", "r", "sigma", "max_periods", "phi", "v", "num_impacts"]),
            ('singularity_set', ["omega", "r", "sigma", "max_periods", "num_points"]),
            ('doa', ["omega", "r", "sigma", "max_periods", "max_velocity", "n_v_increments", "n_phi_increments"])
        ])

    def add_functions(self, lib: ImposcIF) -> None:
        for action, names in self._actions.items():
            args = self._parameters.args(names)
            args.extend([("outfile", "Path"), ("errorfile", "Path")])
            lib.add_function(f"map_{action}", "bool", args)

    def info(self) -> dict:
        result = dict()

        for action, names in self._actions.items():
            result[action] = self._parameters.action_info(names)

        return result
  

class ImposcActions:

    def __init__(self):
        self._cache = ImageCache()
        self._actions = ActionCollection()
        self._imposclib = ImposcIF()
        self._actions.add_functions(self._imposclib)

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

