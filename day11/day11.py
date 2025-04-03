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
    for i in range(blinks):
        # I <3 gross nested list comprehensions.
        input_data = [n for n1, n2 in
                      [((1, None)
                        if (n == 0)
                        else ((n // (10 ** (math.ceil(math.log10(n+1)) // 2)),
                               n % (10 ** (math.ceil(math.log10(n+1)) // 2)))
                              if (math.ceil(math.log10(n+1)) % 2 == 0)
                              else (n * 2024, None)
                              )
                        ) for n in input_data
                       ] for n in (n1, n2) if n is not None]
    return len(input_data)


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
