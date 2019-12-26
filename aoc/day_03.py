import enum


class Direction(enum.Enum):
    Up = "U"
    Left = "L"
    Down = "D"
    Right = "R"


class Wire:
    def __init__(self, path: str):
        self.segments = dict()
        steps = path.split(",")
        (x, y) = (0, 0)
        wire_length = 0
        for step in steps:
            d = step[0]
            l = int(step[1:])
            for i in range(l):
                wire_length += 1
                if d == Direction.Up.value:
                    y += 1
                elif d == Direction.Left.value:
                    x -= 1
                elif d == Direction.Down.value:
                    y -= 1
                elif d == Direction.Right.value:
                    x += 1
                if (x, y) not in self.segments:
                    self.segments[(x, y)] = wire_length

    @property
    def coordinates(self):
        return set(self.segments.keys())


def part_1(data: str) -> int:
    wires = [Wire(path.strip()) for path in data.split("\n") if path]
    intersections = set(wires[0].coordinates)
    for wire in wires[1:]:
        intersections = intersections.intersection(wire.coordinates)
    return list(sorted(map(lambda xy: sum(map(abs, xy)), intersections)))[0]


def part_2(data: str) -> int:
    wires = [Wire(path.strip()) for path in data.split("\n") if path]
    intersections = set(wires[0].coordinates)
    for wire in wires[1:]:
        intersections = intersections.intersection(wire.coordinates)
    distances = dict()
    for intersection in intersections:
        distances[intersection] = sum(wire.segments[intersection] for wire in wires)
    return list(sorted(distances.values()))[0]
