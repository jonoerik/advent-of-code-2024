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
    # Convert to a [(value, run-length] representation.
    data = [(i // 2 if i % 2 == 0 else None, v) for i, v in enumerate(input_data) if v != 0]

    # Compact the disk.
    while True:
        while data[-1][0] is None:
            del data[-1]

        try:
            i = [v for v, _ in data].index(None)
        except ValueError:
            break

        dest_length = data[i][1]
        source_length = data[-1][1]
        if dest_length < source_length:
            data[i] = (data[-1][0], dest_length)
            data[-1] = (data[-1][0], source_length - dest_length)
        elif dest_length == source_length:
            data[i] = (data[-1][0], dest_length)
            del data[-1]
        else:
            data[i] = (data[-1][0], source_length)
            data.insert(i + 1, (None, dest_length - source_length))
            del data[-1]

    assert None not in [v for v, _ in data]

    # Calculate the checksum.
    i = 0
    total = 0
    for v, r in data:
        total += v * sum(range(i, i + r))
        i += r

    return total

def part2(input_data: InputType) -> ResultType:
    pass
