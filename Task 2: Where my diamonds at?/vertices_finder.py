import numpy as np

# To account for pixel inaccuracies
MIN_RATIO: float = 0.96
MAX_RATIO: float = 1.04


class VerticesFinder:
    def __init__(self, image: np.ndarray, target: int, initial_vertex: tuple[int, int], direction: str) -> None:
        self._image: np.ndarray = image
        self._height, self._width = image.shape
        self._target: int = target
        self._initial_vertex = initial_vertex
        self._start_x, self._start_y = initial_vertex
        self._direction: str = direction

    def _top(self) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        # Find bottom vertex
        y: int = self._start_y
        for y in range(self._start_y, self._height):
            if self._image[y, self._start_x] != self._target:
                break
        bottom_vertex: tuple[int, int] = self._start_x, y - 1

        mid_y: int = (self._start_y + bottom_vertex[1]) // 2

        # Find right vertex
        x = self._start_x
        for x in range(self._start_x, self._width):
            if self._image[mid_y, x] != self._target:
                break
        right_vertex: tuple[int, int] = x - 1, mid_y

        # Find left vertex
        left_vertex: tuple[int, int] = 2 * self._start_x - right_vertex[0], mid_y

        return bottom_vertex, left_vertex, right_vertex

    def _left(self) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        # Find right vertex
        x: int = self._start_x
        for x in range(self._start_x, self._width):
            if self._image[self._start_y, x] != self._target:
                break
        right_vertex: tuple[int, int] = x - 1, self._start_y

        mid_x: int = (self._start_x + right_vertex[0]) // 2

        # Find bottom vertex
        y = self._start_y
        for y in range(self._start_y, self._height):
            if self._image[y, mid_x] != self._target:
                break
        bottom_vertex: tuple[int, int] = mid_x, y - 1

        # Find top vertex
        top_vertex: tuple[int, int] = mid_x, 2 * self._start_y - bottom_vertex[1]

        return top_vertex, bottom_vertex, right_vertex

    def vertices(self) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        # top, bottom, left, right
        match self._direction:
            case 'top':
                bottom_vertex, left_vertex, right_vertex = self._top()
                return self._initial_vertex, bottom_vertex, left_vertex, right_vertex

            case 'left':
                top_vertex, bottom_vertex, right_vertex = self._left()
                return top_vertex, bottom_vertex, self._initial_vertex, right_vertex

            case _:
                raise ValueError(f'Invalid direction: {self._direction}')

    def aspect_ratio(self) -> float:
        top_vertex, bottom_vertex, left_vertex, right_vertex = self.vertices()
        width = right_vertex[0] - left_vertex[0]
        height = bottom_vertex[1] - top_vertex[1]
        try:
            ratio: float = round(width / height, 2)
        except ZeroDivisionError:
            return 0

        # To account for pixel inaccuracies
        if MIN_RATIO < ratio < MAX_RATIO:
            return 1

        return ratio
