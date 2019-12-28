import numpy


class Image:
    colormap = {
        0: "█",
        1: "░",
    }

    def __init__(self, w: int, h: int, pixels: numpy.ndarray):
        self.layers = numpy.array(pixels).reshape((len(pixels) // (w * h), h, w))

    @classmethod
    def from_str(cls, w: int, h: int, data: str):
        return cls(w, h, list(map(int, data.strip())))

    def composite(self) -> numpy.ndarray:
        def render(stack):
            return stack[numpy.argmax(stack < 2)]
        return numpy.apply_along_axis(render, 0, self.layers)

    def composite_pretty(self, colormap=None) -> str:
        colormap = colormap or self.colormap
        composite = self.composite()
        printout = numpy.ndarray(composite.shape, dtype=str)
        for k, v in colormap.items():
            printout = numpy.where(composite == k, v, printout)
        return "\n".join("".join(l) for l in printout.tolist())


def part_1(data: str) -> int:
    image = Image.from_str(25, 6, data)
    i = numpy.argmax(numpy.count_nonzero(image.layers, axis=(1, 2)))
    layer = image.layers.take(indices=i, axis=0)
    counts = dict(zip(*numpy.unique(layer, return_counts=True)))
    return counts[1] * counts[2]


def part_2(data: str) -> str:
    return Image.from_str(25, 6, data).composite_pretty()
