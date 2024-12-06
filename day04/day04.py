#!/usr/bin/env python3

from pathlib import Path

InputType = list[str]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [line.strip() for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    def is_xmas(r, c, dr, dc) -> bool:
        return "".join([input_data[r + i * dr][c + i * dc] for i in range(4)]) == "XMAS"

    height = len(input_data)
    width = len(input_data[0])

    return [is_xmas(r, c, dr, dc) for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for r in range(height) for c in range(width)
            if 0 <= c + 3 * dc < width and 0 <= r + 3 * dr < height].count(True)


def part2(input_data: InputType) -> ResultType:
    return ["".join([input_data[r + dr][c + dc] for dr, dc in [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)]])
            in ["MMASS", "SMASM", "SSAMM", "MSAMS"]
            for r in range(1, len(input_data) - 1) for c in range(1, len(input_data[0]) - 1)
            ].count(True)
