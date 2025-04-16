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


def part1(input_data: InputType, cheat_max_duration: int = 2,
          min_saving: int = 100, exact_saving: int | None = None) -> ResultType:
    """ If exact_saving is not None, find the number of cheat options that save exactly that many picoseconds.
    Otherwise, find the number of cheats that save at least min_saving picoseconds."""
    start = [(r, c) for r, row in enumerate(input_data)
             for c, tile in enumerate(row) if tile == Tile.START][0]
    end = [(r, c) for r, row in enumerate(input_data)
           for c, tile in enumerate(row) if tile == Tile.END][0]

    def time_path(s: tuple[int, int], e: tuple[int, int]) -> tuple[int, dict[tuple[int, int], int]]:
        """Find length of shortest path from start s to end e using Dijkstra's Algorithm.
        Also find all tiles that are closer to end, or equally close (including the end tile itself), and return the
        distance to these tiles.
        Result is (distance_to_end, {(r, c) -> distance_from_start})."""

        # {(r, c): cost}.
        to_visit: dict[tuple[int, int], int] = {s: 0}
        # {(r, c): cost}.
        visited: dict[tuple[int, int], int] = {}
        end_cost = None
        while to_visit:
            r, c = min(to_visit, key=to_visit.get)
            cost = to_visit[(r, c)]
            del to_visit[(r, c)]
            if (r, c) == e:
                end_cost = cost
            if end_cost is not None and cost > end_cost:
                # Delay exiting the algorithm until we're sure all points of equal distance to e have been counted.
                break
            assert (r, c) not in visited
            visited[(r, c)] = cost

            for next_r, next_c in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if (0 <= next_r < len(input_data)
                        and 0 <= next_c < len(input_data[0])
                        and (next_r, next_c) not in visited
                        and input_data[next_r][next_c] != Tile.WALL):
                    if (next_r, next_c) not in to_visit or to_visit[(next_r, next_c)] > cost + 1:
                        to_visit[(next_r, next_c)] = cost + 1

        assert end_cost is not None
        return end_cost, visited

    # Find the time to traverse the maze without cheating, and the distance to all points reachable in this time.
    honest_time, start_dists = time_path(start, end)
    time_goal = range(honest_time - exact_saving, honest_time - exact_saving + 1) \
        if exact_saving is not None \
        else range(0, honest_time - min_saving + 1)
    # Filter out points not reachable in our required (with cheats) time.
    start_dists = {pos: cost for pos, cost in start_dists.items() if cost < time_goal.stop}
    # Calculate distance from sufficiently close points to the end.
    _, end_dists = time_path(end, start)
    end_dists = {pos: cost for pos, cost in end_dists.items() if cost < time_goal.stop}

    # For all potential combinations of cheat start position and cheat end position, check the total distance from
    # start to end using this cheat. If the cheat is of the permitted duration, and enables reaching the end in the
    # required time, count it towards the total.
    result = 0
    for cheat_start in start_dists:
        for cheat_end in end_dists:
            cheat_duration = abs(cheat_start[0] - cheat_end[0]) + abs(cheat_start[1] - cheat_end[1])
            if cheat_duration <= cheat_max_duration and \
                    (start_dists[cheat_start] + cheat_duration + end_dists[cheat_end]) in time_goal:
                result += 1
    return result


def part2(input_data: InputType, min_saving: int = 100, exact_saving: int | None = None) -> ResultType:
    return part1(input_data, 20, min_saving, exact_saving)
