from aoc.computer import Computer


def part_1(data) -> int:
    c = Computer.from_str(data)
    c.state[1] = 12
    c.state[2] = 2
    return c.execute()


def part_2(data) -> int:
    c = Computer.from_str(data)
    for i in range(100):
        for j in range(100):
            c.state[1] = i
            c.state[2] = j
            result = c.execute()
            if result == 19690720:
                return 100 * c.state[1] + c.state[2]
            c.reset()
    raise RuntimeError("no result found")
