def hasadjacent(n: int):
    s = str(n)
    for i in range(len(s) - 1):
        if s[i] == s[i+1]:
            return True
    return False


def hasadjacent_picky(n: int):
    s = str(n)
    if len(s) > 2 and s[0] == s[1] != s[2] or s[-3] != s[-2] == s[-1]:
        return True
    for i in range(1, len(s) - 1):
        if s[i-1] != s[i] == s[i+1] != s[i+2]:
            return True
    return False


def nondecreasing(n: int):
    digits = map(int, str(n))
    prev = 0
    for d in digits:
        if prev > d:
            return False
        prev = d
    return True


def part_1(data: str) -> int:
    lower, upper = map(int, data.split("-"))
    return sum(
        1
        for n in range(lower, upper+1)
        if hasadjacent(n) and nondecreasing(n)
    )


def part_2(data: str) -> int:
    lower, upper = map(int, data.split("-"))
    return sum(
        1
        for n in range(lower, upper+1)
        if hasadjacent_picky(n) and nondecreasing(n)
    )
