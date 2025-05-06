#!/usr/bin/env python3

from enum import Enum
import itertools
from pathlib import Path

InputType = list[str]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [line.strip() for line in f.readlines()]


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

# For each robot, the current key the robot is positioned to actuate. Direction pad robots are all combined into a
# sub-tuple, to allow handling of different counts of these robots.
SearchState = tuple[tuple[DirKey, ...], NumKey]


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
    result_dirpad_robots = []
    prev_key = k
    for dirpad_robot in s[0]:
        result_dirpad_robot = next_dir_key(dirpad_robot, prev_key)
        if result_dirpad_robot is None:
            return None
        result_dirpad_robots.append(result_dirpad_robot)
        if prev_key != DirKey.A:
            result_dirpad_robots += s[0][len(result_dirpad_robots):]
            return tuple(result_dirpad_robots), s[1]
        prev_key = result_dirpad_robot
    else:
        assert len(result_dirpad_robots) == len(s[0])
        result_numpad_robot = next_num_key(s[1], prev_key)
        if result_numpad_robot is None:
            return None
        return tuple(result_dirpad_robots), result_numpad_robot


def calculate_heuristic(end_key: NumKey, s: SearchState) -> int:
    """Return a heuristic estimate of the number of manual button presses to reach the required end_key on the num pad,
    from SearchState. While this heuristic must be admissible, this A* implementation allows visited nodes to be
    revisited if a lower cost path is found, so the heuristic isn't required to be consistent."""
    # Gray code representation of robot states.
    # Highest bit is 1 if the numpad robot is on end_key, 0 otherwise.
    # Next bit is the dirpad robot immediately before the numpad robot, 0 if the robot is on the activate key,
    # 1 otherwise.
    # Successive dirpad robots are successive grey code bits, with the LSB being the first robot (after the manually
    # actuated dirpad).
    g = 1 if s[1] == end_key else 0
    for dk in reversed(s[0]):
        g <<= 1
        if dk != DirKey.A:
            g += 1

    # Convert gray code representation to binary number.
    # Wikipedia contributors. (2025, March 10). Gray code. In Wikipedia, The Free Encyclopedia.
    # Retrieved 10:43, May 3, 2025, from https://en.wikipedia.org/w/index.php?title=Gray_code&oldid=1279704355
    mask = g
    while mask:
        mask >>= 1
        g ^= mask

    # Take 2^bits - 1 - g, which is the bare minimum number of inputs to get to the desired end state.
    result = 2 ** (len(s[0]) + 1) - 1 - g
    return result


shortest_sequence_next_key_memo: dict[tuple[NumKey, NumKey, int], int] = {}


def shortest_sequence_next_key(start_key: NumKey, end_key: NumKey, dir_pad_robot_count: int) -> int:
    """Use A* algorithm to find the length of the shortest sequence of manual number presses to input, to move the
    number pad robot from key start_key to key end_key (without actuating it). All other robots start on A, and will
    end on A as well."""
    global shortest_sequence_next_key_memo
    if (start_key, end_key, dir_pad_robot_count) in shortest_sequence_next_key_memo:
        return shortest_sequence_next_key_memo[(start_key, end_key, dir_pad_robot_count)]

    start_state = ((DirKey.A,) * dir_pad_robot_count, start_key)
    # {state: (current cost, current cost + heuristic, predecessor)}
    to_visit: dict[SearchState, tuple[int, int, SearchState | None]] = \
        {start_state: (0, calculate_heuristic(end_key, start_state), None)}
    # {state: (lowest cost to reach found so far, predecessor)}
    visited: dict[SearchState, tuple[int, SearchState]] = {}

    while to_visit:
        current_state = min(to_visit, key=lambda x: to_visit[x][1])
        cost, total_heuristic, predecessor = to_visit[current_state]
        del to_visit[current_state]
        if current_state == ((DirKey.A,) * dir_pad_robot_count, end_key):
            shortest_sequence_next_key_memo[(start_key, end_key, dir_pad_robot_count)] = cost

            #TODO comment
            # Reconstruct and print the path of states.
            path: list[SearchState] = [current_state]
            next_path_node = predecessor
            while next_path_node is not None:
                path.append(next_path_node)
                next_path_node = visited[next_path_node][1]
            print(f"{"A" if start_key is AKey else start_key} -> {"A" if end_key is AKey else end_key}")
            print("\t" + "\n\t".join([
                "-".join([{DirKey.A: "A", DirKey.UP: "^", DirKey.DOWN: "v", DirKey.LEFT: "<", DirKey.RIGHT: ">"}[dirkey]
                          for dirkey in path_node[0]]
                         ) + "-" +
                ("A" if path_node[1] is AKey else str(path_node[1])) for path_node in reversed(path)]))

            return cost

        # Allow states to be revisited, as our heuristic may not be consistent, and a better path to an earlier visited
        # state could be found later.
        assert current_state not in visited or visited[current_state][0] > cost
        visited[current_state] = (cost, predecessor)

        for key in DirKey:
            next_to_visit = next_state(current_state, key)
            if next_to_visit is None or (next_to_visit in visited and visited[next_to_visit][0] <= cost + 1):
                continue
            if next_to_visit not in to_visit or to_visit[next_to_visit][0] > cost + 1:
                to_visit[next_to_visit] = (cost + 1,
                                           cost + 1 + calculate_heuristic(end_key, next_to_visit),
                                           current_state)

    # Should have found a suitable sequence before exhausting the search space.
    assert False


def shortest_sequence(code: str, dir_pad_robot_count: int) -> int:
    """Find the length of the shortest sequence of manual button presses to input the required code into the numeric
    keypad."""
    # Add up the cost of transitioning to each next numpad key, and the cost of pressing each key.
    return sum(
        [shortest_sequence_next_key(AKey if start_key == "A" else int(start_key),
                                    AKey if end_key == "A" else int(end_key),
                                    dir_pad_robot_count)
         for start_key, end_key in itertools.pairwise("A" + code)]
    ) + len(code)


def part1(input_data: InputType) -> ResultType:
    assert all([x.endswith("A") and x[:-1].isnumeric() for x in input_data])
    return sum([int(x[:-1]) * shortest_sequence(x, 2) for x in input_data])


#TODO remove rounds arg
def part2(input_data: InputType, rounds=25) -> ResultType:
    assert all([x.endswith("A") and x[:-1].isnumeric() for x in input_data])
    return sum([int(x[:-1]) * shortest_sequence(x, rounds) for x in input_data])
