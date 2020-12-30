
from time import time_ns
from typing import List, Tuple, Union
from pathlib import Path

def unique_file_name(extension: str) -> str:
    """ Returns a unique file name with the specified `extension` """
    return f"{time_ns()}.{extension}"

def files_size(files: List[Tuple[Union[str, Path], int]]) -> int:
    """ Sums the sizes from a supplied list of file sizes """
    return sum([x[1] for x in files])

if __name__ == "__main__":
    print(unique_file_name("txt"))