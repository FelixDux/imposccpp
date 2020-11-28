from pathlib import Path
from time import time_ns

def unique_file_name(extension: str):
    return f"{time_ns()}.{extension}"

def files_size(files):
    return sum([x[1] for x in files])


class ImageCache:
    """
    Generates image file names on request and maintains a cache of image files.
    """

    def __init__(self, _directory: str = "images", _size_limit: int = 1024 * 1024 * 512):
        self._directory = _directory
        self._size_limit = _size_limit
        self._cache_path = Path(_directory).absolute()

        if not self._cache_path.exists():
            self._cache_path.mkdir()

    @property
    def cache_path(self) -> str:
        return self._cache_path
        
    def offer_new_file(self, extension: str = "png"):
        """
        Ensures the cache is below the size limit and returns a new unique file name.
        """
        self.reduce_cache()
        return self.new_file_name(extension)

    def new_file_name(self, extension: str = "png"):
        """
        Returns a path for a new file in the cache with 
        an extension specified in `extension`.
        """
        return self._cache_path / unique_file_name(extension)

    def reduce_cache(self):
        files = self.cache_files()

        cache_size = files_size(files)

        while cache_size > self._size_limit:
            file_pair = files.pop()

            file_pair[0].unlink()
            cache_size -= file_pair[1]

    def cache_files(self):
        p = self._cache_path.glob('**/*')
        
        return list([(x, x.stat().st_size) for x in p if x.is_file()])
