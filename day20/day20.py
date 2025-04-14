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


def part1(input_data: InputType, min_saving: int = 100, exact_saving: int | None = None) -> ResultType:
    """ If exact_saving is not None, find the number of cheat options that save exactly that many picoseconds.
    Otherwise, find the number of cheats that save at least min_saving picoseconds."""

    # Check that the maze doesn't contain any areas like this:
    #
    # #####
    # ...##
    # ###.#
    # ###.#
    #
    # If the maze contains areas where two diagonally adjacent open areas aren't connected by at least one open tile,
    # then a valid cheat could save time by moving between those two open tiles. Each of the two cheat steps would move
    # in a different direction. Without these areas in the maze, all valid time-saving cheats take two steps in the
    # same direction, from open tile to wall to open tile.
    for r in range(len(input_data)):
        for c in range(len(input_data[0])):
            if input_data[r][c] != Tile.WALL:
                for r2, c2 in [(r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]:
                    if 0 <= r2 < len(input_data) and 0 <= c2 < len(input_data[0]):
                        if input_data[r2][c2] != Tile.WALL:
                            assert input_data[r][c2] != Tile.WALL or input_data[r2][c] != Tile.WALL
    # Ensure the maze is completely surrounded by walls.
    assert (all([input_data[r][0] == Tile.WALL and input_data[r][-1] == Tile.WALL
                 for r in range(len(input_data))])
            and all([input_data[0][c] == Tile.WALL and input_data[-1][c] == Tile.WALL
                     for c in range(len(input_data[0]))]))

    def time_to_end(cheat_tile: tuple[int, int] | None) -> int:
        start_r, start_c = [(r, c) for r, row in enumerate(input_data)
                            for c, tile in enumerate(row) if tile == Tile.START][0]

        # Find length of shortest path to exit using Dijkstra's Algorithm.
        # {(r, c): length}.
        to_visit: dict[tuple[int, int], int] = {(start_r, start_c): 0}
        # {(r, c)}.
        visited: set[tuple[int, int]] = set()

        while to_visit:
            r, c = min(to_visit, key=to_visit.get)
            cost = to_visit[(r, c)]
            del to_visit[(r, c)]
            if input_data[r][c] == Tile.END:
                return cost
            visited.add((r, c))

            for next_r, next_c in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if (0 <= next_r < len(input_data)
                        and 0 <= next_c <= len(input_data[0])
                        and (next_r, next_c) not in visited):
                    if input_data[next_r][next_c] != Tile.WALL or (next_r, next_c) == cheat_tile:
                        if (next_r, next_c) not in to_visit or to_visit[(next_r, next_c)] > cost + 1:
                            to_visit[(next_r, next_c)] = cost + 1

    result = 0
    honest_time = time_to_end(None)
    for r in range(1, len(input_data) - 1):
        for c in range(1, len(input_data[0]) - 1):
            if (input_data[r][c] == Tile.WALL
                 and ((input_data[r-1][c] != Tile.WALL and input_data[r+1][c] != Tile.WALL)
                      or (input_data[r][c-1] != Tile.WALL and input_data[r][c+1] != Tile.WALL))):
                time_saved = honest_time - time_to_end((r, c))
                if exact_saving is not None:
                    if time_saved == exact_saving:
                        result += 1
                else:
                    if time_saved >= min_saving:
                        result += 1

    return result


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
