#!/usr/bin/env python3

from enum import Enum
from pathlib import Path

InputType = list[str]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [line.strip() for line in f.readlines()]


def part1(input_data: InputType) -> ResultType:
    class AKeyType:
        pass
    AKey = AKeyType()
    NumKey = int | AKeyType
    class DirKey(Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3
        A = 4

    # For each robot, the current key the robot is positioned to actuate, and the string of keys pressed on the final
    # number pad.
    SearchState = tuple[DirKey, DirKey, NumKey, str]

    def next_num_key(current_key: NumKey, dir_key: DirKey) -> NumKey | None:
        """Given a current number pad key position, find the adjacent key in the direction of dir_key, or None
        if no valid key is in that direction."""
        keypad = [
            [7, 8, 9],
            [4, 5, 6],
            [1, 2, 3],
            [None, 0, AKey]
        ]
        pos = [(r, c) for r, row in enumerate(keypad) for c, x in enumerate(row) if x == current_key][0]
        dr, dc = {DirKey.UP: (-1, 0),
                  DirKey.DOWN: (1, 0),
                  DirKey.LEFT: (0, -1),
                  DirKey.RIGHT: (0, 1),
                  DirKey.A: (0, 0)}[dir_key]
        pos = (pos[0] + dr, pos[1] + dc)
        if 0 <= pos[0] < len(keypad) and 0 <= pos[1] < len(keypad[0]):
            return keypad[pos[0]][pos[1]]
        else:
            return None

    def next_dir_key(current_key: DirKey, dir_key: DirKey) -> DirKey | None:
        """Given a current directional pad key position, find the adjacent key in the direction of dir_key, or None
        if no valid key is in that direction."""
        keypad = [
            [None, DirKey.UP, DirKey.A],
            [DirKey.LEFT, DirKey.DOWN, DirKey.RIGHT]
        ]
        pos = [(r, c) for r, row in enumerate(keypad) for c, x in enumerate(row) if x == current_key][0]
        dr, dc = {DirKey.UP: (-1, 0),
                  DirKey.DOWN: (1, 0),
                  DirKey.LEFT: (0, -1),
                  DirKey.RIGHT: (0, 1),
                  DirKey.A: (0, 0)}[dir_key]
        pos = (pos[0] + dr, pos[1] + dc)
        if 0 <= pos[0] < len(keypad) and 0 <= pos[1] < len(keypad[0]):
            return keypad[pos[0]][pos[1]]
        else:
            return None

    def next_state(s: SearchState, k: DirKey) -> SearchState | None:
        """Given a current state, and a direction key manually pressed on the first number pad, return the resulting
        state of the system. Return None if the keypress leads to an invalid state."""
        a = next_dir_key(s[0], k)
        if a is None:
            return None
        if k == DirKey.A:
            b = next_dir_key(s[1], a)
            if b is None:
                return None
            if a == DirKey.A:
                c = next_num_key(s[2], b)
                if c is None:
                    return None
                if b == DirKey.A:
                    return (a, b, c, s[3] + ("A" if c == AKey else str(c)))
                else:
                    return (a, b, c, s[3])
            else:
                return (a, b, s[2], s[3])
        else:
            return (a, s[1], s[2], s[3])

    def shortest_sequence(code: str) -> int:
        """Use Dijkstra's Algorithm to find the length of the shortest sequence of manual button presses to input the
        required code into the numeric keypad."""
        to_visit: dict[SearchState, int] = {(DirKey.A, DirKey.A, AKey, ""): 0}
        visited: set[SearchState] = set()

        while to_visit:
            current_state = min(to_visit, key=to_visit.get)
            cost = to_visit[current_state]
            del to_visit[current_state]
            if current_state[3] == code:
                return cost
            assert current_state not in visited
            visited.add(current_state)

            for key in DirKey:
                next_to_visit = next_state(current_state, key)
                if next_to_visit is None or next_to_visit in visited:
                    continue
                if not code.startswith(next_to_visit[3]):
                    continue
                if next_to_visit not in to_visit or to_visit[next_to_visit] > cost + 1:
                    to_visit[next_to_visit] = cost + 1

        # Should have found a suitable sequence before exhausting the search space.
        assert False

    assert all([x.endswith("A") and x[:-1].isnumeric() for x in input_data])
    return sum([int(x[:-1]) * shortest_sequence(x) for x in input_data])


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
