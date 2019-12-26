def solve(data, fuel):
    return sum(fuel(int(line)) for line in data.splitlines())


def part_1(data):
    return solve(data, lambda n: n // 3 - 2)


def part_2(data):
    def fuel(n):
        result = 0
        while n > 6:
            n = n // 3 - 2
            result += n
        return result
    return solve(data, fuel)
