#!/usr/bin/env python3

import collections
import itertools
from pathlib import Path

InputType = list[str]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [line.strip() for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    # Map of antenna ID to list of locations (row, col) where that antenna is present.
    antennas: dict[str: list[tuple[int, int]]] = collections.defaultdict(list)
    for r, row in enumerate(input_data):
        for c, antenna_id in enumerate(row):
            if antenna_id != ".":
                antennas[antenna_id].append((r, c))

    antinodes = set()
    height = len(input_data)
    width = len(input_data[0])

    for antenna_id, positions in antennas.items():
        for a, b in itertools.permutations(positions, 2):
            antinode_r = a[0] + 2 * (b[0] - a[0])
            antinode_c = a[1] + 2 * (b[1] - a[1])
            if 0 <= antinode_r < height and \
                0 <= antinode_c < width:
                antinodes.add((antinode_r, antinode_c))

    return len(antinodes)


def part2(input_data: InputType) -> ResultType:
    pass
