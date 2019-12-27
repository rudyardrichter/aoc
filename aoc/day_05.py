from aoc.computer import Computer


def part_1(data: str) -> int:
    c = Computer.from_str(data)
    c.input([1])
    c.execute()
    return c.read_output()
