#!/usr/bin/env python3

from collections.abc import Iterator
import math
from pathlib import Path

InputType = list[int]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        lines = f.readlines()
        assert len(lines) == 1
        return [int(n) for n in lines[0].strip().split()]


def part1(input_data: InputType, blinks: int = 25) -> ResultType:
    def next_blink(it: Iterator[int]) -> Iterator[int]:
        for v in it:
            if v == 0:
                yield 1
            else:
                num_digits = math.ceil(math.log10(v + 1))
                if num_digits % 2 == 0:
                    m = 10 ** (num_digits // 2)
                    yield v // m
                    yield v % m
                else:
                    yield v * 2024

    stones = iter(input_data)
    for _ in range(blinks):
        stones = next_blink(stones)
    return sum([1 for _ in stones])


def part2(input_data: InputType, blinks: int = 75) -> ResultType:
    return part1(input_data, blinks)
