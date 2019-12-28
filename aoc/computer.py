from collections import deque
import enum
from itertools import permutations
from typing import List, Optional


class OpCode(enum.Enum):
    add = 1
    mul = 2
    inp = 3
    out = 4
    jit = 5
    jif = 6
    clt = 7
    ceq = 8
    arb = 9
    hcf = 99

    @property
    def n_params(self):
        if self is self.add or self is self.mul or self is self.clt or self is self.ceq:
            return 3
        if self is self.jit or self is self.jif:
            return 2
        if self is self.inp or self is self.out or self is self.arb:
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
    relative = 2


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
    wait = enum.auto()


class Computer:

    def __init__(self, instructions: List[int], debug=False):
        self.state = instructions
        self.original_state = list(self.state)
        self.ip = 0
        self.rb = 0
        self.inputs = None
        self.outputs = []
        self.debug = debug

    @classmethod
    def from_str(cls, data: str, **kwargs):
        return cls(list(map(int, data.strip().split(","))), **kwargs)

    def input(self, inputs):
        self.inputs = deque(inputs)
        return self

    def send_input(self, n: int):
        if self.inputs is None:
            self.inputs = deque([])
        self.inputs.append(n)
        return self

    def get_input(self):
        try:
            return self.inputs.popleft()
        except IndexError:
            return None

    def output(self, n):
        self.outputs.append(n)

    def read_output(self):
        return self.outputs

    @property
    def return_value(self):
        return self.outputs[-1]

    def step(self):
        op = Operation.from_int(self.state[self.ip])

        def add_mem():
            self.state.extend(0 for _ in range(len(self.state)))

        def addr(n):
            value = read(self.ip+n+1)
            if op.modes[n] is Mode.relative:
                return self.rb + value
            return value

        def read(n) -> int:
            while n > len(self.state):
                add_mem()
            return self.state[n]

        def write(n, value):
            a = addr(n)
            while a > len(self.state):
                add_mem()
            self.state[a] = value

        def param(n):
            value = read(self.ip+n+1)
            if op.modes[n] is Mode.position:
                return read(value)
            elif op.modes[n] is Mode.relative:
                return read(self.rb + value)
            else:  # Mode.immediate
                return value

        if self.debug:
            debug_msg = (
                op.opcode.name
                + " ".join([""] + [str(param(i)) for i in range(op.opcode.n_params)])
            )
            if op.opcode.n_params:
                debug_msg += " (" + ", ".join(mode.name for mode in op.modes) + ")"
            print(debug_msg)

        if op.opcode.is_binary_op():
            write(2, op.opcode.f(param(0), param(1)))
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
            write(2, 1 if result else 0)
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.inp:
            inp = self.get_input()
            if inp is None:
                return StepResult.wait
            write(0, inp)
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.out:
            self.output(param(0))
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode is OpCode.arb:
            self.rb += param(0)
            self.ip += op.opcode.n_params + 1
            return StepResult.ok
        elif op.opcode == OpCode.hcf:
            return StepResult.stop
        else:
            return StepResult.err

    def execute(self) -> StepResult:
        step = StepResult.ok
        while step == StepResult.ok:
            step = self.step()
        self.step_result = step
        return step

    def reset(self):
        self.ip = 0
        self.state = list(self.original_state)


class Amplifier:
    def __init__(self, data: str, n: int):
        self.n = n
        self.data = data
        self.computers = None

    def setup_amps(self, settings: List[int]):
        self.computers = [_ for _ in range(self.n)]
        for i in range(self.n):
            self.computers[i] = Computer.from_str(self.data).input([settings[i]])

    def run_amplifiers(self, first_input: int = 0):
        self.computers[0].send_input(first_input)
        for i in range(1, self.n):
            self.computers[i-1].execute()
            self.computers[i].send_input(self.computers[i-1].return_value)
        self.computers[-1].execute()

    def solve(self) -> int:
        best = 0
        for settings in permutations(range(self.n)):
            self.setup_amps(settings)
            self.run_amplifiers()
            best = max(best, self.computers[self.n-1].return_value)
        return best

    def solve_feedback(self) -> int:
        best = 0
        for settings in permutations(range(5,5+self.n)):
            self.setup_amps(settings)
            self.run_amplifiers()
            last_step: Optional[StepResult] = None
            while last_step != StepResult.stop:
                self.run_amplifiers(first_input=self.computers[-1].return_value)
                last_step = self.computers[-1].step_result
                best = max(best, self.computers[self.n-1].return_value)
        return best
