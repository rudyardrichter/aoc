from aoc.day_08 import Image


def test_image_indices():
    image = Image.from_str(3, 2, "123456789012")
    assert image.layers[0][1][0] == 4
