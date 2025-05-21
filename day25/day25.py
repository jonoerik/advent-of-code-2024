#!/usr/bin/env python3

from pathlib import Path


KeyType = list[int]
LockType = list[int]
# (keys, locks, total tumbler height)
InputType = tuple[list[KeyType], list[LockType], int]
ResultType = int


def load(input_path: Path) -> InputType:
    keys: list[KeyType] = []
    locks: list[LockType] = []

    with open(input_path) as f:
        lines = []
        while True:
            line = f.readline().strip()
            if line:
                lines.append(line)
            else:
                if not lines:
                    break

                schematic_height = len(lines)
                schematic_width = len(lines[0])
                assert all([len(row) == schematic_width for row in lines])

                # Transpose.
                lines = [[lines[c][r] for c in range(schematic_height)] for r in range(schematic_width)]
                if lines[0][0] == "#":
                    locks.append([row.count("#") - 1 for row in lines])

                elif lines[0][0] == ".":
                    keys.append([row.count("#") - 1 for row in lines])

                else:
                    # Unexpected character in input.
                    assert False

                lines = []

    return keys, locks, schematic_height


def part1(input_data: InputType) -> ResultType:
    keys, locks, tumbler_height = input_data

    def key_fits(k: KeyType, l: LockType) -> bool:
        return all(a + b < tumbler_height - 1 for a, b in zip(k, l))

    return sum(1 if key_fits(key, lock) else 0 for key in keys for lock in locks)


def part2(input_data: InputType) -> None:
    # Part 2 considered solved once all previous puzzles have been solved.
    return None
