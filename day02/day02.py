#!/usr/bin/env python3

from pathlib import Path

InputType = list[list[int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [list(map(int, line.strip().split())) for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    def is_safe(l: list[int]) -> bool:
        pairs = list(zip(l[:-1], l[1:]))
        return all(map(lambda x: x[0] < x[1] <= x[0] + 3, pairs)) or all(map(lambda x: x[1] < x[0] <= x[1] + 3, pairs))

    return [is_safe(record) for record in input_data].count(True)


def part2(input_data: InputType) -> ResultType:
    pass
