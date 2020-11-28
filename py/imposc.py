from image_cache import ImageCache
from imposclib import ImposcIF
from pathlib import Path


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


if __name__ == "__main__":
    from PIL import Image

    actions = ImposcActions()

    image_file = actions.impacts(2.8, 0.8, 0, 100, 0.5, 0, 1000)

    if image_file.exists():
        Image.open(image_file).show()

