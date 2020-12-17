
from time import time_ns

def unique_file_name(extension: str):
    return f"{time_ns()}.{extension}"

def files_size(files):
    return sum([x[1] for x in files])