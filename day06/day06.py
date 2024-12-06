#!/usr/bin/env python3

from enum import IntEnum
from pathlib import Path

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
FloorMapType = list[list[bool]]  # True: blocked, False: open space.
GuardType = tuple[int, int, Direction]  # The guard's starting row, starting column, and initial direction.
InputType = tuple[FloorMapType, GuardType]
ResultType = int


def load(input_path: Path) -> InputType:
    floor_map = []
    guard = None
    direction_map = {"^": Direction.UP, ">": Direction.RIGHT, "v": Direction.DOWN, "<": Direction.LEFT}

    with open(input_path) as f:
        for row, line in enumerate(f.readlines()):
            line = line.strip()
            for d in direction_map.keys():
                if d in line:
                    assert guard is None
                    guard = (row, line.index(d), direction_map[d])
            floor_map.append([c == "#" for c in line])

    assert guard is not None
    return floor_map, guard


def part1(input_data: InputType) -> ResultType:
    visited_positions = set()

    floor_map, (guard_r, guard_c, guard_dir) = input_data
    dr, dc = {Direction.UP: (-1, 0),
              Direction.RIGHT: (0, 1),
              Direction.DOWN: (1, 0),
              Direction.LEFT: (0, -1)
              }[guard_dir]

    while 0 <= guard_r < len(floor_map) and 0 <= guard_c < len(floor_map[0]):
        visited_positions.add((guard_r, guard_c))
        if 0 <= guard_r + dr < len(floor_map) and 0 <= guard_c + dc < len(floor_map[0]) \
                and floor_map[guard_r + dr][guard_c + dc]:
            # Turn 90 degrees to the right.
            dr, dc = dc, dr * -1
        else:
            guard_r += dr
            guard_c += dc

    return len(visited_positions)


def part2(input_data: InputType) -> ResultType:
    pass
