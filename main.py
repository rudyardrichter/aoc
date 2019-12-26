import argparse
import importlib


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("day", metavar="DAY", type=int, help="which day to run")
    parser.add_argument("part", metavar="PART", type=int, help="which part to run")
    return parser.parse_args()


def main():
    args = parse_args()
    day = "day_{:02}".format(args.day)
    part = f"part_{args.part}"
    solve = getattr(importlib.import_module(f"aoc.{day}"), part)
    with open(f"inputs/{day}/input") as f:
        print(solve(f.read()))


if __name__ == '__main__':
    main()
