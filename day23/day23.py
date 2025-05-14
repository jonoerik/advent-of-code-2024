#!/usr/bin/env python3

import collections
import itertools
from pathlib import Path

InputType = list[tuple[str, str]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [tuple(line.strip().split("-", 2)) for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    graph: dict[str: set[str]] = collections.defaultdict(set)
    for a, b in input_data:
        graph[a].add(b)
        graph[b].add(a)

    trios: set[frozenset[str]] = set()
    for a in graph.keys():
        if a.startswith("t"):
            for b, c in itertools.combinations(graph[a], 2):
                if c in graph[b]:
                    trios.add(frozenset((a, b, c)))

    return len(trios)


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
