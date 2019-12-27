import pytest

from aoc.computer import Computer


@pytest.mark.parametrize(
    ("data", "answer"),
    [
        ("1,0,0,0,99", 2),
        ("1,1,1,4,99,5,6,0,99", 30),
        ("1,9,10,3,2,3,11,0,99,30,40,50", 3500),
    ],
)
def test_computer_v1(data, answer):
    c = Computer.from_str(data)
    assert c.execute() == answer


@pytest.mark.parametrize(
    ("data", "answer"),
    [
        ("1002,4,3,4,33", 1002),
        ("1101,100,-1,4,0", 1101),
    ],
)
def test_computer_v2(data, answer):
    c = Computer.from_str(data)
    assert c.execute() == answer


@pytest.mark.parametrize(
    ("data", "inp", "out"),
    [
        ("3,0,4,0,99", [1234], [1234]),
        ("3,0,1,0,0,2,4,2,99", [2], [4]),
    ]
)
def test_computer_io(data, inp, out):
    c = Computer.from_str(data)
    c.input(inp)
    c.execute()
    assert c.outputs == out
