from image_cache import ImageCache
from imposclib import ImposcIF
from pathlib import Path
from PIL import Image
from lib_errors import LibErrors
from dataclasses import dataclass, asdict
from typing import Tuple, List, Optional, Union, Dict


@dataclass
class ActionParameter:
    group: str
    name: str
    description: str
    range: str
    type: str
    label: str
    defaultValue: Optional[Union[int, float]]

    def toArg(self) -> Tuple[str, str]:
        return (self.name, self.type)

    def validate(self, value: str) ->  Optional[Union[int, float, str]]:
        result = None

        try:
            if self.type in ["float", "double"]:
                result = float(value)
            elif self.type in ["int", "uint"]:
                result = int(value)
            else:
                result = value
        except ValueError:
            result = None

        return result


class ActionParameterCollection:
    def __init__(self):
        self._groups = dict()
        self._parameters = dict()

        self.add(ActionParameter(group="Parameters", name = 'omega', description = 'Forcing frequency', range = 'positive', type = 'double', label = 'ω', defaultValue=None))
        self.add(ActionParameter(group="Parameters", name = 'sigma', description = 'Obstacle offset', range = '', type = 'double', label = 'σ', defaultValue=None))
        self.add(ActionParameter(group="Parameters", name = 'r', description = 'Coefficient of restitution', range = 'non-negative', type = 'double', label = 'r', defaultValue=None))
    
        self.add(ActionParameter(group="Initial", name = 'phi', description = 'Phase (modulo 1)', range = 'circle', type = 'double', label = 'φ', defaultValue=0.5))
        self.add(ActionParameter(group="Initial", name = 'v', description = 'Velocity', range = 'non-negative', type = 'double', label = 'v', defaultValue=0))
    
        self.add(ActionParameter(group="Options", name = 'max_periods', description = 'Max forcing periods between impacts', range = 'positive', type = 'uint', label = 'P', defaultValue=100))
        self.add(ActionParameter(group="Options", name = 'num_impacts', description = 'Number of impacts to plot', range = 'positive-big', type = 'uint', label = 'N', defaultValue=20000))
        self.add(ActionParameter(group="Options", name = 'num_points', description = 'Number points along singularity set', range = 'positive-big', type = 'uint', label = 'M', defaultValue=5000))
        self.add(ActionParameter(group="Options", name = 'n_phi_increments', description = 'Number of phase increments for DOA plot', range = 'positive-big', type = 'uint', label = 'Nφ', defaultValue=200))
        self.add(ActionParameter(group="Options", name = 'n_v_increments', description = 'Number of velocity increments for DOA plot', range = 'positive-big', type = 'uint', label = 'Nv', defaultValue=200))
        self.add(ActionParameter(group="Options", name = 'max_velocity', description = 'Maximum velocity for DOA plot', range = 'non-negative', type = 'double', label = 'vmax', defaultValue=4.0))
        self.add(ActionParameter(group="Options", name = 'n_iterations', description = 'Number of impacts to detect orbit in DOA plot', range = 'positive', type = 'uint', label = 'Ni', defaultValue=500))

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

    def validate(self, name: str, value: str) ->  Optional[Union[int, float, str]]:
        if name in self._parameters:
            return self._parameters[name].validate(value)
        else:
            return None


class ActionCollection:
    def __init__(self):
        self._parameters = ActionParameterCollection()
        self._actions = dict([
            ('impacts', (["omega", "r", "sigma", "max_periods", "phi", "v", "num_impacts"], "Scatter plot on the impact surface", "Scatter")),
            ('singularity_set', (["omega", "r", "sigma", "max_periods", "num_points"], "Plot points on the impact surface which map to zero-velocity impacts", "Singularity set")),
            ('doa', (["omega", "r", "sigma", "max_periods", "max_velocity", "n_v_increments", "n_phi_increments", "n_iterations"], "Domain of attraction plot on the impact surface", "DOA plot"))
        ])

    def add_functions(self, lib: ImposcIF) -> None:
        for action_name, action in self._actions.items():
            names = action[0]
            args = self._parameters.args(names)
            args.extend([("outfile", "Path"), ("errorfile", "Path")])
            lib.add_function(f"{action_name}", "bool", args)

    def info(self) -> dict:
        result = dict()

        for action_name, action in self._actions.items():
            names = action[0]
            result[action_name] = dict([("description", action[1]), ("label", action[2]), ("groups", self._parameters.action_info(names))])

        return result

    def validate(self, name: str, value: str) ->  Optional[Union[int, float, str]]:
        return self._parameters.validate(name, value)
  

class ImposcActions:

    def __init__(self):
        self._cache = ImageCache()
        self._actions = ActionCollection()
        self._imposclib = ImposcIF()
        self._actions.add_functions(self._imposclib)

    def info(self) -> dict:
        return self._actions.info()

    def validate(self, args: Dict[str,str]) -> Tuple[Dict[str, Optional[Union[int, float, str]]], List[str]]:
        validated = dict(map(lambda pair: (pair[0], self._actions.validate(pair[0], pair[1])), args.items()))

        outcome = list(map(lambda elem: f"Parameter {elem[0]} was supplied with an invalid value {args[elem[0]]}", filter(lambda pair: pair is None, validated.items())))

        return validated, outcome


    def impacts(self, **kwargs) -> Path:
        errors = LibErrors()
        try:
            outfile = str(self._cache.offer_new_file())
            if self._imposclib.impacts(outfile=outfile.encode('utf-8'), errorfile=errors.errorFile.encode('utf-8'), **kwargs):
                return outfile
            else:
                return errors.errorPath
        except TypeError as e:
            errors.put(f"{e}")
            return errors.errorPath

    def singularity_set(self, **kwargs) -> Path:
        errors = LibErrors()
        try:
            outfile = str(self._cache.offer_new_file())
            if self._imposclib.singularity_set(outfile=outfile.encode('utf-8'), errorfile=errors.errorFile.encode('utf-8'), **kwargs):
                return outfile
            else:
                return errors.errorPath
        except TypeError as e:
            errors.put(f"{e}")
            return errors.errorPath

    def doa(self, **kwargs) -> Path:
        errors = LibErrors()
        try:
            outfile = str(self._cache.offer_new_file())
            if self._imposclib.doa(outfile=outfile.encode('utf-8'), errorfile=errors.errorFile.encode('utf-8'), **kwargs):
                return outfile
            else:
                return errors.errorPath
        except TypeError as e:
            errors.put(f"{e}")
            return errors.errorPath
            

def do_and_show(image_file):
    if isinstance(image_file, str):
        image_file = Path(image_file)

    if image_file.exists():
        if image_file.suffix == ".txt":
            print(image_file.read_text())
        else:
            Image.open(image_file).show()
        
def alias_args(args: dict, alias_to: str, alias_from: str="num_impacts") -> dict:
    aliaser = lambda arg_kv : (alias_to, arg_kv[1]) if arg_kv[0]==alias_from else arg_kv
    
    return dict(map(aliaser, args.items()))

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
    parser.add_argument("-m", "--max-velocity", type=float, help="Maximum velocity for DOA plot", default=4.0)
    parser.add_argument("-i", "--num-impacts", default=4000, type=int, help="The number of impacts")
    parser.add_argument("--n-v-increments", default=100, type=int, help="The number of v increments for a doa plot")
    parser.add_argument("--n-phi-increments", default=100, type=int, help="The number of phase increments for a doa plot")

    args = vars(parser.parse_args())

    actions = ImposcActions()

    plot = args.pop('plot')

    if plot == "impacts":
        do_and_show(actions.impacts(**args))

    elif plot == "singularity-set":
        do_and_show(actions.singularity_set(**alias_args(args, alias_to="num_points")))

    elif plot == "doa":
        do_and_show(actions.doa(**alias_args(args, alias_to="n_iterations")))

