import pytest

from aoc.day_12 import System


examples = [
    "<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>\n",
    "<x=-8, y=-10, z=0>\n<x=5, y=5, z=10>\n<x=2, y=-7, z=3>\n<x=9, y=-8, z=-3>\n",
]


@pytest.mark.parametrize(
    ("data", "steps", "energy"),
    [
        (examples[0], 10, 179),
        (examples[1], 100, 1940),
    ],
)
def test_system_energy(data, steps, energy):
    assert System.from_str(data).step(steps).energy == energy


@pytest.mark.parametrize(
    ("data", "period"),
    [
        (examples[0], 2772),
        (examples[1], 4686774924),
    ],
)
def test_system_period(data, period):
    assert System.from_str(data).period() == period
