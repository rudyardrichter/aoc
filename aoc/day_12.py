from typing import List, Optional, Tuple

import numpy


class System:
    def __init__(self, positions: List[Tuple[int, int, int]]):
        self.x = numpy.array(positions)
        self.v = numpy.zeros(self.x.shape, dtype=int)

    @classmethod
    def from_str(cls, data: str):
        return cls([
            [
                int(coordinate.split(",")[0].split("=")[-1])
                for coordinate in line.strip("<>").split(",")
            ]
            for line in data.strip().splitlines()
        ])

    def step(self, n: Optional[int] = 1) -> "System":
        for _ in range(n):
            for i in range(len(self.x)):
                for j in range(len(self.x)):
                    self.v[i] += numpy.sign(self.x[j] - self.x[i])
            for i in range(len(self.x)):
                self.x[i] += self.v[i]
        return self

    @property
    def energy(self) -> int:
        u = numpy.sum(numpy.absolute(self.x), axis=1)
        k = numpy.sum(numpy.absolute(self.v), axis=1)
        return numpy.sum(u * k)

    def period(self) -> int:
        """
        very
        slow
        """
        period = numpy.zeros(self.x.shape[1], dtype=int)
        self.step()
        x_0 = numpy.copy(self.x)
        v_0 = numpy.copy(self.v)
        i = 0
        while not period.all():
            self.step()
            i += 1
            match = numpy.concatenate((self.x == x_0, self.v == v_0)).all(axis=0)
            period[numpy.argwhere(numpy.logical_and(match, period == 0))] = i
        return numpy.lcm.reduce(period)


def part_1(data: str) -> int:
    return System.from_str(data).step(1000).energy


def part_2(data: str) -> int:
    return System.from_str(data).period()
