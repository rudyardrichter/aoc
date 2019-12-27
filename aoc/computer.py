import enum
from typing import List


class OpCode(enum.Enum):
    add = 1
    mul = 2
    inp = 3
    out = 4
    hcf = 99

    @property
    def n_params(self):
        if self is self.add or self is self.mul:
            return 3
        if self is self.inp or self is self.out:
            return 1
        return 0

    @property
    def f(self):
        if self is self.add:
            return lambda a, b: a + b
        elif self is self.mul:
            return lambda a, b: a * b
        return None


class Mode(enum.Enum):
    position = 0
    immediate = 1


class Operation:
    def __init__(self, opcode, modes: List[int]):
        self.opcode = opcode
        self.modes = modes

    @classmethod
    def from_int(cls, n):
        opcode = OpCode(n % 100)
        modes = []
        for i in range(2, 2+opcode.n_params):
            modes.append(Mode(n // 10 ** i % 10))
        return cls(opcode, modes)


class StepResult(enum.Enum):
    ok = enum.auto()
    stop = enum.auto()
    err = enum.auto()


class Computer:

    def __init__(self, instructions: List[int]):
        self.state = instructions
        self.original_state = list(self.state)
        self.ip = 0
        self.outputs = []

    @classmethod
    def from_str(cls, data: str):
        return cls(list(map(int, data.strip().split(","))))

    def input(self, inputs):
        self.inputs = inputs
        self.inputs.reverse()

    def get_input(self):
        return self.inputs.pop()

    def output(self, n):
        self.outputs.append(n)

    def read_output(self):
        return self.outputs

    def param(self, value, mode):
        if mode is Mode.position:
            return self.state[value]
        return value

    def step(self):
        op = Operation.from_int(self.state[self.ip])
        if op.opcode is OpCode.add or op.opcode is OpCode.mul:
            a = self.param(self.state[self.ip+1], op.modes[0])
            b = self.param(self.state[self.ip+2], op.modes[1])
            c = self.state[self.ip+3]
            self.state[c] = op.opcode.f(a, b)
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.inp:
            self.state[self.state[self.ip+1]] = self.get_input()
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.out:
            self.output(self.state[self.state[self.ip+1]])
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode == OpCode.hcf:
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
