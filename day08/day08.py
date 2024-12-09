#!/usr/bin/env python3

import collections
import itertools
from pathlib import Path

# Map of antenna ID to list of locations (row, col) where that antenna is present, and map width and height.
InputType = tuple[dict[str, list[tuple[int, int]]], tuple[int, int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        antenna_layout = [line.strip() for line in f.readlines()]

    antennas: dict[str, list[tuple[int, int]]] = collections.defaultdict(list)
    for r, row in enumerate(antenna_layout):
        for c, antenna_id in enumerate(row):
            if antenna_id != ".":
                antennas[antenna_id].append((r, c))
    return antennas, (len(antenna_layout[0]), len(antenna_layout))


def part1(input_data: InputType) -> ResultType:
    antinodes = set()
    antennas, (width, height) = input_data

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
