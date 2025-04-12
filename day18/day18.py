#!/usr/bin/env python3

from pathlib import Path

InputType = list[tuple[int, int]]
ResultType1 = int
ResultType2 = str


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [(int(x), int(y)) for x, y in [line.strip().split(",", 1) for line in f.readlines()]]


def length_to_exit(corrupted_bytes: InputType, coord_max: int) -> int | None:
    # Return the length of the path to the exit after the given simulated bytes have been corrupted, or None if no
    # path is possible.
    mem: list[list[bool]] = [[False for _ in range(coord_max + 1)] for _ in range(coord_max + 1)]
    # Simulate memory corruption.
    for x, y in corrupted_bytes:
        mem[y][x] = True

    # Print memory state.
    # print("\n".join(["".join("#" if x else "." for x in line) for line in mem]))

    # Find length of shortest path to exit using Dijkstra's Algorithm.
    # {(x, y): cost}.
    to_visit: dict[tuple[int, int], int] = {(0, 0): 0}
    # {(x, y)}.
    visited: set[tuple[int, int]] = set()
    while to_visit:
        x, y = min(to_visit, key=to_visit.get)
        cost = to_visit[(x, y)]
        del to_visit[(x, y)]
        if (x, y) == (coord_max, coord_max):
            return cost
        visited.add((x, y))
        for next_x, next_y in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if (0 <= next_x <= coord_max
                    and 0 <= next_y <= coord_max
                    and (next_x, next_y) not in visited
                    and not mem[next_y][next_x]):
                if (next_x, next_y) not in to_visit or to_visit[(next_x, next_y)] > cost + 1:
                    to_visit[(next_x, next_y)] = cost + 1

    # If this is reached, no path exists to the exit.
    return None


def part1(input_data: InputType, coord_max: int = 70, simulated_bytes: int = 1024) -> ResultType1:
    result = length_to_exit(input_data[:simulated_bytes], coord_max)
    if result is None:
        assert False
    return result


def part2(input_data: InputType, coord_max: int = 70) -> ResultType2:
    for i in range(len(input_data)+1):
        if length_to_exit(input_data[:i], coord_max) is None:
            return f"{input_data[i-1][0]},{input_data[i-1][1]}"

    # If this is reached, the exit is never blocked by a corrupted byte.
    assert False
