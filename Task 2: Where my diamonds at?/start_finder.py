import numpy as np


class StartFinder:
    def __init__(self, image: np.ndarray, target: int) -> None:
        self._image: np.ndarray = image
        self._height, self._width = image.shape
        self._target: int = target

    def top(self) -> tuple[int, int]:
        for y in range(self._height):
            for x in range(self._width):
                if self._image[y][x] == self._target:
                    return x, y
        raise ValueError('Target not found')

    def left(self) -> tuple[int, int]:
        for x in range(self._width):
            for y in range(self._height):
                if self._image[y][x] == self._target:
                    return x, y
        raise ValueError('Target not found')
