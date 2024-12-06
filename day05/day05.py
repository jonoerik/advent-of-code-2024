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


def update_valid(rules: list[RuleType], update: UpdateType) -> bool:
    for r in rules:
        if r[0] in update and r[1] in update and update.index(r[1]) < update.index(r[0]):
            return False
    return True


def part1(input_data: InputType) -> ResultType:
    rules, updates = input_data
    total = 0

    for update in updates:
        if update_valid(rules, update):
            total += update[len(update) // 2]

    return total


def part2(input_data: InputType) -> ResultType:
    rules, updates = input_data
    total = 0

    def fix_update(u: list[int]) -> list[int]:
        # The rules can be treated as edges in a directed graph, where a->b means that a must be sorted before b in
        # valid updates.
        # To fix an update, take the subset of rules a->b where both a and b appear in the update, construct the graph
        # of those rules. A valid update will be a topological ordering of the nodes. As we expect a valid update to
        # exist, a topological ordering will be possible (i.e. the rules subset graph will be a DAG).

        # Use Kahn's Algorithm to find the topological ordering.
        # Topological Sorting, Wikipedia, accessed 2024-12-06
        # https://en.wikipedia.org/w/index.php?title=Topological_sorting&oldid=1258030734#Kahn's_algorithm
        graph = [(a, b) for a, b in rules if a in u and b in u]
        source_nodes = {a for a,b in graph}
        destination_nodes = {b for a,b in graph}
        L = []
        S = source_nodes - destination_nodes
        while S:
            n = S.pop()
            L.append(n)
            for m in {x for x in destination_nodes if (n, x) in graph}:
                graph.remove((n, m))
                if m not in [b for a, b in graph]:
                    S.add(m)

        assert not graph
        return L

    for update in updates:
        if not update_valid(rules, update):
            update = fix_update(update)
            total += update[len(update) // 2]

    return total
