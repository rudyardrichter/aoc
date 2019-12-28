from aoc.computer import Amplifier


def part_1(data: str) -> int:
    return Amplifier(data, 5).solve()


def part_2(data: str) -> int:
    return Amplifier(data, 5).solve_feedback()
