import pytest

from aoc.graphics import coordinates_to_ascii


@pytest.mark.parametrize(
    ("coordinates", "output"),
    [
        (
            {(0, 0): 1, (5, 0): 1, (5, 5): 1, (10, 5): 1},
            (
                "█████░████░\n"
                "███████████\n"
                "███████████\n"
                "███████████\n"
                "███████████\n"
                "░████░█████"
            ),
        ),
    ]
)
def test_to_ascii(coordinates, output):
    assert coordinates_to_ascii(coordinates) == output
