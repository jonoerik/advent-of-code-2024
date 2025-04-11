#!/usr/bin/env python3

from enum import Enum
from pathlib import Path

class Tile(Enum):
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3

InputType = list[list[Tile]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [[{".": Tile.EMPTY,
                  "#": Tile.WALL,
                  "S": Tile.START,
                  "E": Tile.END
                  }[c] for c in line.strip()] for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    start_r, start_c = [(r, c) for r, row in enumerate(input_data) for c, tile in enumerate(row) if tile == Tile.START][0]
    start_dr, start_dc = (0, 1)

    def cost_to_end(r: int, c: int, dr: int, dc: int, visited: set[tuple[int, int, int, int]]) -> int | None:
        """Return the smallest cost to get to the end tile, from (r, c), facing direction (dr, dc),
        or None if this path shouldn't be considered because it revisits a previous state."""
        if input_data[r][c] == Tile.END:
            return 0

        if input_data[r][c] == Tile.WALL:
            return None

        if (r, c, dr, dc) in visited:
            return None

        options = [a + b for a, b in [
            (1, cost_to_end(r + dr, c + dc, dr, dc, visited | {(r, c, dr, dc)})),
            (1000, cost_to_end(r, c, -dc, dr, visited | {(r, c, dr, dc)})),
            (1000, cost_to_end(r, c, dc, -dr, visited | {(r, c, dr, dc)}))
        ] if b is not None]
        return min(options) if options else None

    return cost_to_end(start_r, start_c, start_dr, start_dc, set())


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
