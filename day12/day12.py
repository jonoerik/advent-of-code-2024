#!/usr/bin/env python3

from pathlib import Path

InputType = list[str]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [l.strip() for l in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    width = len(input_data[0])
    height = len(input_data)

    def expand_region(start: tuple[int, int]) -> set[tuple[int, int]]:
        to_check: set[tuple[int, int]] = {start}
        checked: set[tuple[int, int]] = set()
        result: set[tuple[int, int]] = set()
        c = input_data[start[0]][start[1]]
        while to_check:
            p = to_check.pop()
            if input_data[p[0]][p[1]] == c:
                result.add(p)
                for next_p in [(p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1)]:
                    if 0 <= next_p[0] < height and 0 <= next_p[1] < width and next_p not in checked:
                        to_check.add(next_p)
            checked.add(p)
        return result

    def find_regions() -> list[set[tuple[int, int]]]:
        to_check = {(r, c) for r in range(height) for c in range(width)}
        regions = []
        while to_check:
            p = to_check.pop()
            r = expand_region(p)
            to_check -= r
            regions.append(r)
        return regions

    def perimeter(r: set[tuple[int, int]]):
        return sum([1 for p in r for adjacent
                    in [(p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1)]
                    if adjacent not in r])

    return sum([perimeter(r) * len(r) for r in find_regions()])


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
