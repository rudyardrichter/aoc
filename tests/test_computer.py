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
    c.execute()
    assert c.state[0] == answer


@pytest.mark.parametrize(
    ("data", "answer"),
    [
        ("1002,4,3,4,33", 1002),
        ("1101,100,-1,4,0", 1101),
    ],
)
def test_computer_v2(data, answer):
    c = Computer.from_str(data)
    c.execute()
    assert c.state[0] == answer


LONG_CMP_PROGRAM = (
    "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
    "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
    "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
)


@pytest.mark.parametrize(
    ("data", "inp", "out"),
    [
        ("3,0,4,0,99", [1234], [1234]),
        ("3,0,1,0,0,2,4,2,99", [2], [4]),
        ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [0], [0]),
        ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [1], [1]),
        ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [100], [1]),
        ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [0], [0]),
        ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [1], [1]),
        ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [100], [1]),
        (LONG_CMP_PROGRAM, [1], [999]),
        (LONG_CMP_PROGRAM, [4], [999]),
        (LONG_CMP_PROGRAM, [8], [1000]),
        (LONG_CMP_PROGRAM, [10], [1001]),
        (LONG_CMP_PROGRAM, [100], [1001]),
    ]
)
def test_computer_io(data, inp, out):
    c = Computer.from_str(data)
    c.input(inp)
    c.execute()
    assert c.outputs == out


@pytest.mark.parametrize(
    ("data", "out"),
    [
        (
            "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
            [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],
        ),
        ("1102,34915192,34915192,7,4,7,99,0", [1219070632396864]),
        ("104,1125899906842624,99", [1125899906842624]),
    ]
)
def test_relative_base(data, out):
    c = Computer.from_str(data, debug=True)
    c.execute()
    assert c.outputs == out
