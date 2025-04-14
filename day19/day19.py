#!/usr/bin/env python3

from pathlib import Path

InputType = tuple[list[str], list[str]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        towels = f.readline().strip().split(", ")
        f.readline()  # Blank line.
        return towels, [line.strip() for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    towels, patterns = input_data

    memo: dict[str, bool] = {}
    def pattern_possible(p: str) -> bool:
        nonlocal memo
        if not p:
            return True

        if p in memo:
            return memo[p]

        result = any([pattern_possible(p[len(t):]) for t in towels if p.startswith(t)])
        memo[p] = result
        return result

    return sum([1 for pattern in patterns if pattern_possible(pattern)])


def part2(input_data: InputType) -> ResultType:
    towels, patterns = input_data

    memo: dict[str, int] = {}
    def ways_to_make(p: str) -> int:
        nonlocal memo
        if not p:
            return 1

        if p in memo:
            return memo[p]

        result = sum([ways_to_make(p[len(t):]) for t in towels if p.startswith(t)])
        memo[p] = result
        return result

    return sum([ways_to_make(pattern) for pattern in patterns])
