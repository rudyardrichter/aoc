import numpy


TAU = 2 * numpy.pi


def angle(p):
    if (p[0], p[1]) == (0, 0):
        return numpy.nan
    result = numpy.arctan2(-p[0], p[1])
    if result < 0:
        result += TAU
    if result > TAU:
        result -= TAU
    return result


class Raycaster:
    map_characters = {"#": 1, ".": 0}

    def __init__(self, space: numpy.ndarray):
        self.space = space
        self.asteroids = numpy.argwhere(self.space.T != 0)

    @classmethod
    def from_str(cls, data: str):
        lines = data.strip().splitlines()
        return cls(numpy.array(
            [[cls.map_characters[c] for c in line] for line in lines]
        ))

    def visible_from(self, a: numpy.ndarray) -> int:
        return numpy.unique(numpy.apply_along_axis(angle, 1, a - self.asteroids)).size

    def best_view(self) -> int:
        return max(map(self.visible_from, self.asteroids)) - 1

    def vaporized_nth(self, n: int) -> (int, int):
        station = self.asteroids[
            numpy.argmax(list(map(self.visible_from, self.asteroids)))
        ]

        def angle_and_norm(p: numpy.ndarray):
            diff = station - p
            return numpy.array(
                [(angle(diff), abs(diff[0]) + abs(diff[1]), p[0], p[1])],
                dtype=[("angle", "f8"), ("dist", "i4"), ("x", "i4"), ("y", "i4")],
            )

        angles = numpy.apply_along_axis(angle_and_norm, 1, self.asteroids)
        order = numpy.argsort(angles, order=("angle", "dist"), axis=0).flatten()
        count = 0
        last_angle = None

        for i in order:
            this_angle = angles[i]["angle"]
            if this_angle == last_angle:
                continue
            last_angle = this_angle
            numpy.delete(angles, (i), axis=0)
            count += 1
            if count == n:
                return (int(angles[i]["x"]), int(angles[i]["y"]))

        raise RuntimeError("no result")


def part_1(data: str) -> int:
    return Raycaster.from_str(data).best_view()


def part_2(data: str) -> int:
    p = Raycaster.from_str(data).vaporized_nth(200)
    return p[0] * 100 + p[1]
