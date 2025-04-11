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

    # A node is (r, c, dr, dc).
    NodeType = tuple[int, int, int, int]
    # Node -> cost dictionary.
    to_visit: dict[NodeType, int] = {(start_r, start_c, start_dr, start_dc): 0}
    visited: set[NodeType] = set()

    # Simple Dijkstra's Algorithm implementation.
    # Could use A*, as using `cost to reach end tile, ignoring walls` is an admissible and consistent heuristic,
    # but this simpler implementation is already sufficiently fast.
    while to_visit:
        current_node = min(to_visit, key=to_visit.get)
        current_cost = to_visit[current_node]
        del to_visit[current_node]
        r, c, dr, dc = current_node
        if input_data[r][c] == Tile.END:
            return current_cost
        visited.add(current_node)

        # Move straight ahead.
        if input_data[r + dr][c + dc] != Tile.WALL:
            next_r = r + dr
            next_c = c + dc
            while (input_data[next_r - dc][next_c + dr] == Tile.WALL
                   and input_data[next_r + dc][next_c - dr] == Tile.WALL
                   and input_data[next_r + dr][next_c + dc] != Tile.WALL):
                # If moving down a corridor, move all the way to the next junction / corner / dead end.
                next_r += dr
                next_c += dc
            dist = abs((r - next_r) + (c - next_c))
            next_node = (next_r, next_c, dr, dc)
            next_cost = current_cost + dist
            if next_node not in visited:
                if next_node not in to_visit or to_visit[next_node] > next_cost:
                    to_visit[next_node] = next_cost

        # Turn left.
        next_node = (r, c, -dc, dr)
        if next_node not in visited:
            if next_node not in to_visit or to_visit[next_node] > current_cost + 1000:
                to_visit[next_node] = current_cost + 1000
        # Turn right.
        next_node = (r, c, dc, -dr)
        if next_node not in visited:
            if next_node not in to_visit or to_visit[next_node] > current_cost + 1000:
                to_visit[next_node] = current_cost + 1000

    assert False

def part2(input_data: InputType) -> ResultType:
    pass  # TODO
