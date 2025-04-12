#!/usr/bin/env python3

from enum import Enum
from pathlib import Path

class Tile(Enum):
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3

InputType = list[list[Tile]]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [[{".": Tile.EMPTY,
                  "#": Tile.WALL,
                  "S": Tile.START,
                  "E": Tile.END
                  }[c] for c in line.strip()] for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    start_r, start_c = [(r, c) for r, row in enumerate(input_data) for c, tile in enumerate(row) if tile == Tile.START][0]
    start_dr, start_dc = (0, 1)

    # A node is (r, c, dr, dc).
    NodeType = tuple[int, int, int, int]
    # Node -> cost dictionary.
    to_visit: dict[NodeType, int] = {(start_r, start_c, start_dr, start_dc): 0}
    visited: set[NodeType] = set()

    # Simple Dijkstra's Algorithm implementation.
    # Could use A*, as using `cost to reach end tile, ignoring walls` is an admissible and consistent heuristic,
    # but this simpler implementation is already sufficiently fast.
    while to_visit:
        current_node = min(to_visit, key=to_visit.get)
        current_cost = to_visit[current_node]
        del to_visit[current_node]
        r, c, dr, dc = current_node
        if input_data[r][c] == Tile.END:
            return current_cost
        visited.add(current_node)

        # Move straight ahead.
        if input_data[r + dr][c + dc] != Tile.WALL:
            next_r = r + dr
            next_c = c + dc
            while (input_data[next_r - dc][next_c + dr] == Tile.WALL
                   and input_data[next_r + dc][next_c - dr] == Tile.WALL
                   and input_data[next_r + dr][next_c + dc] != Tile.WALL):
                # If moving down a corridor, move all the way to the next junction / corner / dead end.
                next_r += dr
                next_c += dc
            dist = abs((r - next_r) + (c - next_c))
            next_node = (next_r, next_c, dr, dc)
            next_cost = current_cost + dist
            if next_node not in visited:
                if next_node not in to_visit or to_visit[next_node] > next_cost:
                    to_visit[next_node] = next_cost

        # Turn left.
        next_node = (r, c, -dc, dr)
        if next_node not in visited:
            if next_node not in to_visit or to_visit[next_node] > current_cost + 1000:
                to_visit[next_node] = current_cost + 1000
        # Turn right.
        next_node = (r, c, dc, -dr)
        if next_node not in visited:
            if next_node not in to_visit or to_visit[next_node] > current_cost + 1000:
                to_visit[next_node] = current_cost + 1000

    assert False

def part2(input_data: InputType) -> ResultType:
    # Use the same approach as part 1, but for each node, track the set of nodes that precede it in any optimal paths.
    start_r, start_c = [(r, c) for r, row in enumerate(input_data) for c, tile in enumerate(row) if tile == Tile.START][0]
    start_dr, start_dc = (0, 1)

    # A node is (r, c, dr, dc).
    NodeType = tuple[int, int, int, int]
    # Node -> cost, set of nodes that lead to this node in any optimal path.
    to_visit: dict[NodeType, tuple[int, set[NodeType]]] = {(start_r, start_c, start_dr, start_dc): (0, set())}
    # Node -> set of nodes that lead to this node in any optimal path.
    visited: dict[NodeType, set[NodeType]] = {}

    def add_to_visit(node: NodeType, cost: int, source: NodeType):
        if node not in visited:
            if node in to_visit:
                if to_visit[node][0] == cost:
                    to_visit[node][1].add(source)
                elif to_visit[node][0] > cost:
                    to_visit[node] = (cost, {source})
            else:
                to_visit[node] = (cost, {source})

    def count_path_cells(end_r: int, end_c: int) -> int:
        to_check: set[NodeType] = {end_node for end_node in visited if end_node[0] == end_r and end_node[1] == end_c}
        checked: set[NodeType] = set()
        while to_check:
            check_node = to_check.pop()
            checked.add(check_node)
            for check_predecessor in visited[check_node]:
                if check_predecessor not in checked:
                    to_check.add(check_predecessor)

        path_nodes = {(c_r, c_c) for c_r, c_c, _, _ in checked}
        # Print the best paths through the map.
        # print("\n".join(["".join(["#" if tile == Tile.WALL else "O" if (r, c) in path_nodes else "."
        #                           for c, tile in enumerate(row)]) for r, row in enumerate(input_data)]))
        return len(path_nodes)

    while to_visit:
        current_node = min(to_visit, key=lambda x: to_visit[x][0])
        current_cost, source_nodes = to_visit[current_node]
        del to_visit[current_node]
        r, c, dr, dc = current_node
        visited[current_node] = source_nodes

        if (input_data[r][c] == Tile.END
                and Tile.END not in [input_data[pending_node[0]][pending_node[1]] for pending_node in to_visit.keys()]):
            return count_path_cells(r, c)

        # Move straight ahead.
        # Only move one tile, as we want all the path tiles to appear in visited, so the final count is correct.
        if input_data[r + dr][c + dc] != Tile.WALL:
            add_to_visit((r + dr, c + dc, dr, dc), current_cost + 1, current_node)

        # Turn left.
        add_to_visit((r, c, -dc, dr), current_cost + 1000, current_node)
        # Turn right.
        add_to_visit((r, c, dc, -dr), current_cost + 1000, current_node)

    assert False
