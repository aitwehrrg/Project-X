import cv2
import numpy as np

BLACK: int = 0
GRAY: int = 28
WHITE: int = 255


class Process:
    def __init__(self, image: np.ndarray, border_value: int, bg_value: int, tolerance: int = 2) -> None:
        self._image = image
        self._border_value = border_value
        self._bg_value = bg_value
        self._TOLERANCE = tolerance  # 2 is the tightest tolerance

    def _remove_border(self) -> None:
        height, width = self._image.shape
        for y in range(height):
            for x in range(width):
                if self._image[y][x] == self._border_value:
                    self._image[y][x] = self._bg_value
        # cv2.imshow('Border Removed', self._image)
        # cv2.waitKey(0)

    # Crops the image to remove the remaining pixels that are not the background
    def _crop(self) -> None:
        height, width = self._image.shape
        # Left crop
        for x in range(width):
            if self._image[0][x] != self._bg_value:
                self._image = self._image[:, x + 1:]
                _, width = self._image.shape
                break
        # Right crop
        for x in range(width - 1, -1, -1):
            if self._image[height - 1][x] != self._bg_value:
                self._image = self._image[:, :x - 1]
                _, width = self._image.shape
                break
        # Top crop
        for y in range(height):
            if self._image[y][0] != self._bg_value:
                self._image = self._image[y + 1:, :]
                height, _ = self._image.shape
                break
        # Bottom crop
        for y in range(height - 1, -1, -1):
            if self._image[y][width - 1] == self._bg_value:
                self._image = self._image[:y - 1, :]
                break
        # cv2.imshow('Cropped', self._image)
        # cv2.waitKey(0)

    def process(self) -> np.ndarray:
        self._remove_border()

        # Remove remnants of the border (salt and pepper noise)
        self._image = cv2.medianBlur(self._image, 3)
        # cv2.imshow('Median Blur', self._image)
        # cv2.waitKey(0)

        self._crop()

        # Remove any pixels that are not the required color
        self._image[self._image > GRAY + self._TOLERANCE] = WHITE
        self._image[self._image < GRAY - self._TOLERANCE] = WHITE
        # cv2.imshow('Median Blur', self._image)
        # cv2.waitKey(0)

        # Convert the image to binary
        _, self._image = cv2.threshold(self._image, 254, 255, cv2.THRESH_BINARY)
        return self._image
