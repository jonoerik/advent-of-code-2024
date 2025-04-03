#!/usr/bin/env python3

from pathlib import Path

# Use None to signify impassable tiles.
InputType = list[list[int | None]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [[int(c) if c != "." else None for c in l.strip()] for l in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    trailheads = [(row, col) for row, line in enumerate(input_data) for col, val in enumerate(line) if val == 0]

    def trail_ends(row, col) -> set[tuple[int, int]]:
        v = input_data[row][col]
        if v is None:
            return set()
        if v == 9:
            return {(row, col)}

        return set.union(set(), *[trail_ends(next_row, next_col) for next_row, next_col
                    in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                    if 0 <= next_row < len(input_data)
                    and 0 <= next_col < len(input_data[0])
                    and input_data[next_row][next_col] == v + 1])

    return sum([len(trail_ends(*trailhead)) for trailhead in trailheads])


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
