import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from image_cache import ImageCache

class ImageCacheTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs(modules_to_reload=[ImageCache])

    def add_to_cache(self, cache: ImageCache, file_size: int) -> str:
        file_name = cache.offer_new_file(extension='dat')
        self.fs.create_file(file_name, st_size=file_size)
        return file_name

    def test_cache_size(self):
        size_unit = 512
        file_size = 2 * size_unit
        limit = 7 * size_unit
        max_files = 1 + int(limit /file_size)

        cache = ImageCache(directory='test_cache', size_limit=limit)

        assert(len(cache.cache_files()) == 0), "Cache not empty on creation"

        for i in range(1, 2*max_files):

            file_name = self.add_to_cache(cache, file_size)

            files = cache.cache_files()

            assert(len(files) == min(i, max_files)), "Cache not removing files"

            assert(files[-1][0] == file_name), "Added file has wrong name"
            assert(files[-1][1] == file_size), "Added file has wrong size"
            assert(file_name not in [f[0] for f in files[:-1]]), "Added file name is not unique"