from pathlib import Path
from typing import List, Tuple, Union

from file_makers import unique_file_name, files_size

class ImageCache:
    """
    Generates image file names on request and maintains a cache of image files.
    """

    def __init__(self, directory: str = "images", size_limit: int = 1024 * 1024 * 512):
        """

        Keyword arguments:

        directory -- the name of a directory to cache the files in (default 'images')
        size_limit -- the maximum total size in bytes of the cached files - old files will be removed to keep the total size below this limit (default 512MB)
        """
        self._directory = directory
        self._size_limit = size_limit
        self._cache_path = Path(directory).absolute()

        if not self._cache_path.exists():
            self._cache_path.mkdir()

    @property
    def cache_path(self) -> Path:
        """ Path to the cache directory """
        return self._cache_path
        
    def offer_new_file(self, extension: str = "png") -> Path:
        """
        Ensures the cache is below the size limit and returns a new unique file name.
        """
        self.reduce_cache()
        return self.new_file_name(extension)

    def new_file_name(self, extension: str = "png") -> Path:
        """
        Returns a path for a new file in the cache with 
        an extension specified in `extension`.
        """
        return self._cache_path / unique_file_name(extension)

    def reduce_cache(self) -> None:
        """
        Removes old files from the cache until the size is below the limit
        """
        files = self.cache_files()

        cache_size = files_size(files)

        while cache_size > self._size_limit:
            file_pair = files.pop()

            file_pair[0].unlink()
            cache_size -= file_pair[1]

    def cache_files(self) -> List[Tuple[Union[str, Path], int]]:
        """ Lists files currently in the cache with their sizes """
        p = self._cache_path.glob('**/*')
        
        return list([(x, x.stat().st_size) for x in p if x.is_file()])
