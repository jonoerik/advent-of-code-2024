#!/usr/bin/env python3

from pathlib import Path

InputType = list[int]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [int(line.strip()) for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    def next_secret(s: int) -> int:
        s ^= s << 6
        s %= 16777216
        s ^= s >> 5
        s %= 16777216
        s ^= s << 11
        s %= 16777216
        return s

    result = 0
    for initial_secret in input_data:
        x = initial_secret
        for _ in range(2000):
            x = next_secret(x)
        result += x
    return result


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
