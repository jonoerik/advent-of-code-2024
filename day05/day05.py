#!/usr/bin/env python3

from pathlib import Path

RuleType = tuple[int, int]  # (a, b) means page a is before page b.
UpdateType = list[int]
InputType = tuple[list[RuleType], list[UpdateType]]
ResultType = int


def load(input_path: Path) -> InputType:
    rules = []
    updates = []
    with open(input_path) as f:
        while line := f.readline():
            line = line.strip()
            if not line:
                break

            rule: tuple[int, int] = tuple([int(x) for x in line.split("|", 1)])
            assert len(rule) == 2
            rules.append(rule)

        while line := f.readline():
            line = line.strip()
            update = [int(x) for x in line.split(",")]
            updates.append(update)

    return rules, updates


def part1(input_data: InputType) -> ResultType:
    rules, updates = input_data
    total = 0

    def update_valid(u: UpdateType) -> bool:
        for r in rules:
            if r[0] in u and r[1] in u and u.index(r[1]) < u.index(r[0]):
                return False
        return True

    for update in updates:
        if update_valid(update):
            total += update[len(update) // 2]

    return total


def part2(input_data: InputType) -> ResultType:
    pass
