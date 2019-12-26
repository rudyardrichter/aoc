import enum
from typing import List


class OpCode(enum.Enum):
    add = enum.auto()
    mul = enum.auto()
    hcf = enum.auto()

    @classmethod
    def from_int(cls, n: int):
        if n == 1:
            return cls.add
        elif n == 2:
            return cls.mul
        elif n == 99:
            return cls.hcf
        else:
            raise ValueError(f"opcode not recognized: {n}")


class StepResult(enum.Enum):
    ok = enum.auto()
    stop = enum.auto()
    err = enum.auto()


class Computer:

    def __init__(self, instructions: List[int]):
        self.state = instructions
        self.original_state = list(self.state)
        self.ip = 0

    def step(self):
        op = OpCode.from_int(self.state[self.ip])
        if op == OpCode.add:
            b, c, d = self.state[self.ip + 1:self.ip + 4]
            self.state[d] = self.state[b] + self.state[c]
            self.ip += 4
            return StepResult.ok
        elif op == OpCode.mul:
            b, c, d = self.state[self.ip + 1:self.ip + 4]
            self.state[d] = self.state[b] * self.state[c]
            self.ip += 4
            return StepResult.ok
        elif op == OpCode.hcf:
            return StepResult.stop
        else:
            return StepResult.err

    def execute(self) -> int:
        step = StepResult.ok
        while step == StepResult.ok:
            step = self.step()
        return self.state[0]

    def reset(self):
        self.ip = 0
        self.state = list(self.original_state)


def part_1(data) -> int:
    instructions = list(map(int, data.strip().split(",")))
    c = Computer(instructions)
    c.state[1] = 12
    c.state[2] = 2
    return c.execute()


def part_2(data) -> int:
    instructions = list(map(int, data.strip().split(",")))
    c = Computer(instructions)
    for i in range(100):
        for j in range(100):
            c.state[1] = i
            c.state[2] = j
            result = c.execute()
            if result == 19690720:
                return 100 * c.state[1] + c.state[2]
            c.reset()
    raise RuntimeError("no result found")
