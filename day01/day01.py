#!/usr/bin/env python3

from pathlib import Path

InputType = tuple[list[int], list[int]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return list(map(list, zip(*[map(int, line.strip().split()) for line in f.readlines()])))


def part1(input_data: InputType) -> ResultType:
    return sum([abs(b - a) for a, b in zip(*map(sorted, input_data))])


def part2(input_data: InputType) -> ResultType:
    pass
