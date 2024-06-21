import cv2
import numpy as np
import process_image as pi
import start_finder as sf
import vertices_finder as vf

BLACK: int = 0
WHITE: int = 255

TEST_CASES_1: tuple[str, str, str] = ('pics/tc1-1.png', 'pics/tc1-2.png', 'pics/tc1-3.png')
TEST_CASES_2: tuple[str, str, str] = ('pics/tc2-1.png', 'pics/tc2-2.png', 'pics/tc2-3.png')

SUIT_DICT: dict[int, str] = {
    0: 'Hearts',
    1: 'Clubs',
    2: 'Spades',
    3: 'Diamonds'
}

VALUE_DICT: dict[int, str] = {
    0: "Ace",
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6',
}


# Traverse the top row
def horizontal_ratios(image: np.ndarray, target: int) -> list[float]:
    start_x, start_y = sf.StartFinder(image, target).left()
    ratios: list[float] = []
    _, width = image.shape
    for x in range(start_x, width):
        if image[start_y][x] == target and image[start_y][x - 1] != target:
            ratio: float = vf.VerticesFinder(image, target, (x, start_y), 'left').aspect_ratio()
            if ratio != 0:
                ratios.append(ratio)
    return ratios


# Traverse the left column
def vertical_ratios(image: np.ndarray, target: int, start_x: int = 0, start_y: int = 0) -> list[float]:
    ratios: list[float] = []
    height, _ = image.shape
    for y in range(start_y, height):
        if image[y][start_x] == target and image[y - 1][start_x] != target:
            ratio: float = vf.VerticesFinder(image, target, (start_x, y), 'top').aspect_ratio()
            if ratio != 0:
                ratios.append(ratio)
    return ratios


# Required function
# Required function
def output(image: np.ndarray, target: int, suit: str | None = None, value: str | None = None) -> str:
    if suit is None:
        suit_ratios: list[float] = horizontal_ratios(image, BLACK)
        suit_min: float = min(suit_ratios)
        suit_max: float = max(suit_ratios)

        # Check the minimum and maximum ratios of the rop row to determine the nature of the card
        if suit_min == 1 and suit_max == 1:  # the card is upside down and not a 6
            image = cv2.flip(image, -1)  # hold the card upright
            return output(image, target, suit, value)  # try again

        if suit_min < 1 and suit_max == 1:  # the card is upside down and a 6
            value = VALUE_DICT[5]  # the card is a 6 (since it is upside down)
            image = cv2.flip(image, -1)  # hold the card upright
            return output(image, target, suit, value)  # try again

        if suit_min < 1 < suit_max:  # the card is upright and an ace
            suit = SUIT_DICT[suit_ratios.index(suit_max) - 1]  # minus 1 because there are 5 diamonds but only 4 suits
            value = VALUE_DICT[0]  # the card is an ace
            return output(image, target, suit, value)

        # the card is upright and not an ace
        suit = SUIT_DICT[suit_ratios.index(suit_max) - 1]  # minus 1 because there are 5 diamonds but only 4 suits

    # if the upright card is not an ace and the upside down card is not a 6
    if value is None:
        top_x, top_y = sf.StartFinder(image, target).top()
        value_ratios = vertical_ratios(image, target, top_x, top_y)
        value = VALUE_DICT[value_ratios.index(min(value_ratios))]

    output_: str = f'{value} of {suit}'
    print(output_)
    cv2.imshow(output_, image)
    cv2.waitKey(0)
    return output_


def main() -> None:
    # Select the test case from here
    # test_cases: tuple[str, str, str] = TEST_CASES_1
    # test_cases: tuple[str, str, str] = TEST_CASES_2

    test_cases: tuple = TEST_CASES_1 + TEST_CASES_2
    result: str = ''
    for test_case in test_cases:
        image = cv2.imread(test_case, cv2.IMREAD_GRAYSCALE)
        image = pi.Process(image, BLACK, WHITE).process()
        result += f'{output(image, BLACK)}, '
    result += '\b\b'  # remove trailing comma and space; on some terminals it may not work
    print(f'Final result: {result}')


if __name__ == '__main__':
    main()
