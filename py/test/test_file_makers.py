import pytest
from file_makers import unique_file_name, files_size

@pytest.mark.parametrize('extension', ['txt','dat'])
def test_file_name(extension):

    name = unique_file_name(extension)

    tokens = name.split('.')

    assert(len(tokens) == 2)

    assert(tokens[-1] == extension)

    assert(tokens[0].isnumeric())

def test_files_size():
    files = [
        ('a', 25),
        ('b', 50),
        ('c', 25)
    ]

    assert(files_size(files) == 100)