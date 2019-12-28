from aoc.computer import Computer


def part_1(data: str) -> int:
    c = Computer.from_str(data).send_input(1)
    c.execute()
    return c.outputs[-1]
