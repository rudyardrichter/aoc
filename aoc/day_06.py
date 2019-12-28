from typing import List, Tuple


class Orbits:
    def __init__(self, orbits: List[Tuple[str, str]]):
        self.orbiters = dict()
        maybe_root = set()
        not_root = set()
        for a, b in orbits:
            o_a = self.index(a)
            o_b = self.index(b)
            o_b.parent = o_a
            o_a.orbiters.add(o_b)
            maybe_root.add(a)
            not_root.add(b)
        root = maybe_root.difference(not_root)
        self.root = self.orbiters[root.pop()]

    @classmethod
    def from_str(cls, data: str):
        return cls(tuple(line.split(")")) for line in data.strip().split("\n"))

    def index(self, name: str):
        if name not in self.orbiters:
            new_tree = OrbitTree(name)
            self.orbiters[name] = new_tree
            return new_tree
        else:
            return self.orbiters[name]

    def transfers_between(self, src: str, dst: str) -> int:
        path_a = [src] + list(o.name for o in self.orbiters[src].parents())
        path_b = [dst] + list(o.name for o in self.orbiters[dst].parents())
        while path_a and path_b:
            a = path_a.pop()
            b = path_b.pop()
            if a != b:
                return len(path_a) + len(path_b)
        return len(self.orbiters[src].parents()) + len(self.orbiters[dst].parents)


class OrbitTree:
    def __init__(self, name: str):
        self.name = name
        self.parent = None
        self.orbiters = set()

    def checksum(self, start=0) -> int:
        return start + sum(o.checksum(start=start+1) for o in self.orbiters)

    def parents(self) -> List["OrbitTree"]:
        result = []
        current = self.parent
        while current:
            result.append(current)
            current = current.parent
        return result


def part_1(data: str) -> int:
    return Orbits.from_str(data).root.checksum()


def part_2(data: str) -> int:
    return Orbits.from_str(data).transfers_between("YOU", "SAN")
