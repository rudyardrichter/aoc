from aoc.computer import Computer, StepResult
from aoc.graphics import coordinates_to_ascii


class PaintersServant:
    def __init__(self, computer: Computer):
        self.x = 0
        self.y = 0
        self.paint = dict()
        self.program = computer
        self.facing = (0, 1)  # direction vector

    def turn(self, direction):
        a, b = self.facing
        if direction == 0:
            self.facing = (-b, a)
        else:
            self.facing = (b, -a)

    def step(self):
        a, b = self.facing
        self.x += a
        self.y += b

    def run(self) -> int:
        step = None
        while step != StepResult.stop:
            self.program.send_input(self.paint.get((self.x, self.y), 0))
            step = self.program.execute()
            color, direction = self.program.outputs[-2:]
            self.paint[(self.x, self.y)] = color
            self.turn(direction)
            self.step()
        return len(self.paint.keys())


def part_1(data: str) -> int:
    return PaintersServant(Computer.from_str(data)).run()


def part_2(data: str) -> str:
    painter = PaintersServant(Computer.from_str(data))
    painter.paint[(0, 0)] = 1
    painter.run()
    return coordinates_to_ascii(painter.paint)
