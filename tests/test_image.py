from aoc.day_08 import Image


def test_image_indices():
    image = Image.from_str(3, 2, "123456789012")
    assert image.layers[0][1][0] == 4


def test_composite():
    image = Image.from_str(2, 2, "0222112222120000")
    assert image.composite().tolist() == [[0, 1], [1, 0]]
    assert image.composite_pretty() == "█░\n░█"
