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
    for _ in range(blinks):
        i = 0
        while i < len(input_data):
            v = input_data[i]
            if v == 0:
                input_data[i] = 1
            else:
                num_digits = math.ceil(math.log10(v+1))
                if num_digits % 2 == 0:
                    m = 10 ** (num_digits // 2)
                    input_data[i] = v // m
                    input_data.insert(i + 1, v % m)
                    i += 1
                else:
                    input_data[i] = v * 2024
            i += 1

    return len(input_data)


def part2(input_data: InputType, blinks: int = 75) -> ResultType:
    return part1(input_data, blinks)
