#!/usr/bin/env python3

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
    # Memo of (stone value, blinks) -> number of stones.
    memo: dict[tuple[int, int], int] = {}
    def total_stones(v: int, b: int) -> int:
        """
        v: value of current stone.
        b: number of blinks to simulate.
        """
        nonlocal memo

        if b == 0:
            return 1

        if (v, b) in memo:
            return memo[(v, b)]

        if v == 0:
            result = total_stones(1, b - 1)
        else:
            num_digits = math.ceil(math.log10(v + 1))
            if num_digits % 2 == 0:
                m = 10 ** (num_digits // 2)
                result = total_stones(v // m, b - 1) + total_stones(v % m, b - 1)
            else:
                result = total_stones(v * 2024, b - 1)
        memo[(v, b)] = result
        return result


    return sum([total_stones(stone, blinks) for stone in input_data])


def part2(input_data: InputType, blinks: int = 75) -> ResultType:
    return part1(input_data, blinks)
