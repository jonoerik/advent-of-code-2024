#!/usr/bin/env python3

from pathlib import Path

InputType = list[str]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [l.strip() for l in f.readlines()]


def expand_region(input_data: InputType, start: tuple[int, int]) -> set[tuple[int, int]]:
    width = len(input_data[0])
    height = len(input_data)

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

def find_regions(input_data: InputType) -> list[set[tuple[int, int]]]:
    width = len(input_data[0])
    height = len(input_data)

    to_check = {(r, c) for r in range(height) for c in range(width)}
    regions = []

    while to_check:
        p = to_check.pop()
        r = expand_region(input_data, p)
        to_check -= r
        regions.append(r)

    return regions


def part1(input_data: InputType) -> ResultType:
    def perimeter(r: set[tuple[int, int]]) -> int:
        return sum([1 for p in r for adjacent
                    in [(p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1)]
                    if adjacent not in r])

    return sum([perimeter(r) * len(r) for r in find_regions(input_data)])


def part2(input_data: InputType) -> ResultType:
    def count_sides(r: set[tuple[int, int]]) -> int:
        result = 0
        # Check top, bottom, left, and right edges.
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            edges = set()
            for p in r:
                # A tile in r forms part of an edge in a given direction, if the adjacent
                # tile in that direction is not in r.
                if (p[0] + d[0], p[1] + d[1]) not in r:
                    edges.add(p)
            for p in edges:
                # An edge tile is counted if it is at a specific end of the edge.
                # e.g. for top edges, if the tile to the right of the current edge tile isn't in edges,
                # then the current tile is counted.
                # For top edges, count only the right-most.
                # For bottom edges, count only the left-most.
                # For left edges, count only the upper-most.
                # For right edges, count only the lower-most.
                if (p[0] + d[1], p[1] - d[0]) not in edges:
                    result += 1
        return result

    return sum([count_sides(r) * len(r) for r in find_regions(input_data)])
