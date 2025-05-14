#!/usr/bin/env python3

import collections
import itertools
from pathlib import Path

InputType = list[tuple[str, str]]
ResultType1 = int
ResultType2 = str


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [tuple(line.strip().split("-", 2)) for line in f.readlines()]


def part1(input_data: InputType) -> ResultType1:
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


def largest_complete_subgraph(graph: dict[str: set[str]], assumed_in_subgraph: set[str]) -> set[str]:
    if len(assumed_in_subgraph) == len(graph):
        assert set(graph.keys()) == assumed_in_subgraph
        return assumed_in_subgraph

    # Choose any node not yet assumed to be in the subgraph, and find the largest subgraphs if we assume n is
    # included / excluded respectively.
    n = next(iter(set(graph.keys()) - assumed_in_subgraph))
    subgraph_with_n = largest_complete_subgraph({k: {n2 for n2 in v if n in graph[n2]}
                                                 for k, v in graph.items()
                                                 if k == n or n in graph[k]},
                                                assumed_in_subgraph | {n})
    subgraph_without_n = largest_complete_subgraph({k: v - {n}
                                                    for k, v in graph.items()
                                                    if k != n},
                                                   assumed_in_subgraph)

    return max(subgraph_with_n, subgraph_without_n, key=len)


def part2(input_data: InputType) -> ResultType2:
    graph: dict[str: set[str]] = collections.defaultdict(set)
    for a, b in input_data:
        graph[a].add(b)
        graph[b].add(a)

    return ",".join(sorted(largest_complete_subgraph(graph, set())))
