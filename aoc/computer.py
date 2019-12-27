import enum
from typing import List


class OpCode(enum.Enum):
    add = 1
    mul = 2
    inp = 3
    out = 4
    jit = 5
    jif = 6
    clt = 7
    ceq = 8
    hcf = 99

    @property
    def n_params(self):
        if self is self.add or self is self.mul or self is self.clt or self is self.ceq:
            return 3
        if self is self.jit or self is self.jif:
            return 2
        if self is self.inp or self is self.out:
            return 1
        return 0

    def f(self, a, b):
        if self is self.add:
            return a + b
        elif self is self.mul:
            return a * b
        elif self is self.clt:
            return a < b
        elif self is self.ceq:
            return a == b
        return None

    def is_binary_op(self):
        return self is self.add or self is self.mul

    def is_cmp(self):
        return self is self.clt or self is self.ceq


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

    def step(self):
        op = Operation.from_int(self.state[self.ip])

        def param(n, addr=False):
            value = self.state[self.ip+n+1]
            if op.modes[n] is Mode.position and not addr:
                return self.state[value]
            return value

        # debug_msg = (
        #     op.opcode.name
        #     + " ".join([str(param(i)) for i in range(op.opcode.n_params)])
        # )

        if op.opcode.is_binary_op():
            self.state[param(2, addr=True)] = op.opcode.f(param(0), param(1))
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.jit:
            if param(0) != 0:
                self.ip = param(1)
            else:
                self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.jif:
            if param(0) == 0:
                self.ip = param(1)
            else:
                self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode.is_cmp():
            result = op.opcode.f(param(0), param(1))
            self.state[param(2, addr=True)] = 1 if result else 0
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.inp:
            self.state[param(0, addr=True)] = self.get_input()
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.out:
            self.output(param(0))
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
