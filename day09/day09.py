#!/usr/bin/env python3

from pathlib import Path

InputType = list[int]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        result = [[int(c) for c in line.strip()] for line in f.readlines()]

    assert len(result) == 1
    return result[0]


def part1(input_data: InputType) -> ResultType:
    # Expand out the dense representation of the disk map.
    data = [c for a in zip([n * [i] for i,n in enumerate(input_data[:-1:2])], [n * [None]for n in input_data[1::2]])
            for b in a for c in b] + ([len(input_data) // 2] * input_data[-1])

    # Compact the filesystem.
    while None in data:
        if data[-1] is None:
            data = data[:-1]
        else:
            data[data.index(None)] = data[-1]
            data = data[:-1]

    # Calculate the checksum.
    return sum([i * x for i, x in enumerate(data)])


def part2(input_data: InputType) -> ResultType:
    pass
