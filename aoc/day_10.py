import numpy


TAU = 2 * numpy.pi


def angle(p):
    if (p[0], p[1]) == (0, 0):
        return numpy.nan
    result = numpy.arctan2(p[0], -p[1])
    if result < 0:
        result += TAU
    if result > TAU:
        result -= TAU
    return result


class Raycaster:
    map_characters = {"#": 1, ".": 0}

    def __init__(self, space: numpy.ndarray):
        self.space = space

    @classmethod
    def from_str(cls, data: str):
        lines = data.strip().splitlines()
        return cls(numpy.array(
            [[cls.map_characters[c] for c in line] for line in lines]
        ))

    def best_view(self) -> int:
        best = 0
        asteroids = numpy.argwhere(self.space != 0)
        for a in asteroids:
            n = numpy.unique(numpy.apply_along_axis(angle, 1, a - asteroids)).size - 1
            best = max(best, n)
        return best


def part_1(data: str) -> int:
    return Raycaster.from_str(data).best_view()
