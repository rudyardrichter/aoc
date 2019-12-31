import pytest

from aoc.day_12 import System


@pytest.mark.parametrize(
    ("data", "steps", "energy"),
    [
        (
            (
                "<x=-1, y=0, z=2>\n"
                "<x=2, y=-10, z=-7>\n"
                "<x=4, y=-8, z=8>\n"
                "<x=3, y=5, z=-1>\n"
            ),
            10,
            179,
        ),
        (
            (
                "<x=-8, y=-10, z=0>\n"
                "<x=5, y=5, z=10>\n"
                "<x=2, y=-7, z=3>\n"
                "<x=9, y=-8, z=-3>\n"
            ),
            100,
            1940,
        )
    ]
)
def test_system_energy(data, steps, energy):
    assert System.from_str(data).step(steps).energy == energy
