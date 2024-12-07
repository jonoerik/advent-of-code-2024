#!/usr/bin/env python3

from pathlib import Path

InputType = list[tuple[int, list[int]]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [(int(a), [int(c) for c in b.split()]) for a, b in [line.strip().split(": ") for line in f.readlines()]]


def part1(input_data: InputType) -> ResultType:
    def solution_possible(result: int, operands: list[int]) -> bool:
        assert len(operands) > 0
        if len(operands) == 1:
            return result == operands[0]

        return solution_possible(result - operands[-1], operands[:-1]) or (result % operands[-1] == 0 and solution_possible(result // operands[-1], operands[:-1]))

    return sum([result for result, operands in input_data if solution_possible(result, operands)])


def part2(input_data: InputType) -> ResultType:
    pass
