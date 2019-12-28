import numpy


class Image:
    def __init__(self, w: int, h: int, pixels: numpy.ndarray):
        self.layers = numpy.array(pixels).reshape((len(pixels) // (w * h), h, w))

    @classmethod
    def from_str(cls, w: int, h: int, data: str):
        return cls(w, h, list(map(int, data.strip())))


def part_1(data: str) -> int:
    image = Image.from_str(25, 6, data)
    i = numpy.argmax(numpy.count_nonzero(image.layers, axis=(1, 2)))
    layer = image.layers.take(indices=i, axis=0)
    counts = dict(zip(*numpy.unique(layer, return_counts=True)))
    return counts[1] * counts[2]
