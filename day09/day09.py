#!/usr/bin/env python3

from pathlib import Path

InputType = list[int]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        result = [[int(c) for c in line.strip()] for line in f.readlines()]

    assert len(result) == 1
    return result[0]


def run_length_representation(input_data: InputType) -> list[tuple[int | None, int]]:
    """Return a [(value, run-length)] representation of the disk, from the dense input format.
    e.g. [3, 2, 4, 1, 1] -> [0, 0, 0, None, None, 1, 1, 1, 1, None, 2] -> [(0, 3), (None, 2), (1, 4), (None, 1), (2, 1)]"""
    return [(i // 2 if i % 2 == 0 else None, v) for i, v in enumerate(input_data) if v != 0]


def calculate_checksum(disk: list[tuple[int | None, int]]) -> int:
    i = 0
    total = 0
    for v, r in disk:
        if v is not None:
            total += v * sum(range(i, i + r))
        i += r

    return total


def part1(input_data: InputType) -> ResultType:
    data = run_length_representation(input_data)

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

    return calculate_checksum(data)


def part2(input_data: InputType) -> ResultType:
    data = run_length_representation(input_data)

    def compact(d):
        first_free_i = 0
        def find_free_space(min_size: int) -> int | None:
            """Return the index of the first free space section in d which is of at least size min_size, or
            None if no such space exists."""
            nonlocal first_free_i
            while d[first_free_i][0] is not None:
                first_free_i += 1

            for i in range(first_free_i, len(d)):
                if d[i][0] is None and d[i][1] >= min_size:
                    return i
            return None

        for v in range(max([v for v, _ in d if v is not None]), -1, -1):
            # Get `[v for v, _ in d].index(v)`, with the search starting at the end of the list.
            src_i = None
            for src_i in range(len(d) - 1, -1, -1):
                if d[src_i][0] == v:
                    break
            src_len = d[src_i][1]
            dest_i = find_free_space(src_len)

            if dest_i is None or dest_i >= src_i:
                continue
            dest_len = d[dest_i][1]

            if dest_len == src_len:
                d[dest_i] = (v, dest_len)
            else:
                assert dest_len > src_len
                d.insert(dest_i, (v, src_len))
                src_i += 1
                d[dest_i + 1] = (None, dest_len - src_len)
            d[src_i] = (None, src_len)

            # Merge empty space around src_i.
            while 0 <= src_i < len(d) - 1 and d[src_i + 1][0] is None:
                src_len += d[src_i + 1][1]
                d[src_i] = (None, src_len)
                del d[src_i + 1]
            while 0 < src_i < len(d) and d[src_i - 1][0] is None:
                src_len += d[src_i - 1][1]
                d[src_i] = (None, src_len)
                del d[src_i - 1]
                src_i -= 1

            # Remove empty space at the end of the disk.
            while d[-1][0] is None:
                del d[-1]

    compact(data)
    return calculate_checksum(data)
