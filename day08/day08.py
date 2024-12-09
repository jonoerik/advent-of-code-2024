#!/usr/bin/env python3

import collections
import itertools
import math
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
    antinodes = set()
    antennas, (width, height) = input_data

    for antenna_id, positions in antennas.items():
        for a, b in itertools.combinations(positions, 2):
            delta_r = b[0] - a[0]
            delta_c = b[1] - a[1]
            n = math.gcd(delta_r, delta_c)
            delta_r = delta_r // n
            delta_c = delta_c // n

            antinode = a
            while 0 <= antinode[0] < height and 0 <= antinode[1] < width:
                antinodes.add(antinode)
                antinode = (antinode[0] - delta_r, antinode[1] - delta_c)

            antinode = a
            while 0 <= antinode[0] < height and 0 <= antinode[1] < width:
                antinodes.add(antinode)
                antinode = (antinode[0] + delta_r, antinode[1] + delta_c)

    return len(antinodes)
