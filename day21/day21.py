#!/usr/bin/env python3

from collections.abc import Callable
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


# A table of the cost to move the current DirPad robot from one key to another.
# {(from_key, to_key): number_of_manual_inputs_required}.
DirPadTable = dict[tuple[DirKey, DirKey], int]
# Costs for moving between keys on the NumPad.
NumPadTable = dict[tuple[NumKey, NumKey], int]


def calculate_table[
        KeyType
    ](
        next_key_function: Callable[[KeyType, DirKey], KeyType | None],
        key_possibilities: set[KeyType],
        prev_table: DirPadTable | None,
        robot_index: int
    ) -> dict[tuple[KeyType, KeyType], int]:
    """
    Use Dijkstra's Algorithm, and a set of movement costs from the previous directional pad robot, to calculate
    the cost of moving this robot between any pair of two keys.

    Whether the current robot is a directional pad robot, or a number pad robot, is dictated by the KeyType generic
    argument, and the next_key_function and key_possibilities arguments.
    KeyType -- The type of variables representing a single robot/keypad's state.
    next_key_function -- Function that when given the current key state, and a direction pad button pressed by the
        previous robot in the chain, gives the resulting key for this robot (or None if the move is invalid).
    key_possibilities -- Set of all possible values the key pad state can take.
    prev_table -- A dictionary of the cost of moving the previous robot in the chain between any two key states.
        If this is the first robot in the chain, i.e. if robot_index == 0, this should be None instead.
    robot_index -- Position of this robot in the chain. 0 is the first robot after the manual keypad, 1 is the robot
        controlled by robot 0's keypad, etc.
    """
    # {(from_key, to_key): number_of_manual_keypresses}
    result: dict[tuple[KeyType, KeyType], int] = {}
    # (previous_robot_key, current_key)
    SearchState = tuple[DirKey, KeyType]
    assert (robot_index == 0) == (prev_table is None)

    for start_key in key_possibilities:
        end_keys_pending = {key for key in key_possibilities}
        # {search_state: cost_to_reach}
        to_visit: dict[SearchState, int] = {(DirKey.A, start_key): 0}
        # {search_state}
        visited: set[SearchState] = set()

        while end_keys_pending and to_visit:
            previous_robot_key, current_key = min(to_visit, key=lambda k: to_visit[k])
            current_cost = to_visit[(previous_robot_key, current_key)]
            del to_visit[(previous_robot_key, current_key)]
            visited.add((previous_robot_key, current_key))
            if previous_robot_key == DirKey.A and current_key in end_keys_pending:
                result[(start_key, current_key)] = current_cost
                end_keys_pending.remove(current_key)

            # Try actuating the previous robot's key, to move the current robot.
            if previous_robot_key is not DirKey.A and next_key_function(current_key, previous_robot_key) is not None:
                next_state = (previous_robot_key, next_key_function(current_key, previous_robot_key))
                next_cost = current_cost + 1
                if next_state not in visited and (next_state not in to_visit or to_visit[next_state] > next_cost):
                    to_visit[next_state] = next_cost

            # Try moving the previous robot to another key.
            for target_prev_robot_key in DirKey:
                if target_prev_robot_key == previous_robot_key:
                    continue
                next_state = (target_prev_robot_key, current_key)
                if robot_index == 0:
                    # If this is the first robot, the 'previous robot' is the manually actuated directional pad,
                    # which can press any key without the cost of moving between them.
                    next_cost = current_cost
                else:
                    next_cost = current_cost + prev_table[(previous_robot_key, target_prev_robot_key)]
                if next_state not in visited and (next_state not in to_visit or to_visit[next_state] > next_cost):
                    to_visit[next_state] = next_cost

        assert not end_keys_pending

    # Cost of transitioning between any two keys should have been calculated.
    assert len(result) == len(key_possibilities) ** 2
    return result


def calculate_dir_pad_table(prev_table: DirPadTable, robot_index: int) -> DirPadTable:
    return calculate_table(next_dir_key, set(DirKey), prev_table, robot_index)


def calculate_num_pad_table(prev_table: DirPadTable, robot_index: int) -> NumPadTable:
    return calculate_table(next_num_key, set(range(10)) | {AKey}, prev_table, robot_index)


def shortest_sequence(code: str, dir_pad_robot_count: int) -> int:
    """Find the length of the shortest sequence of manual button presses to input the required code into the numeric
    keypad."""
    robot_movement_table = None
    for i in range(dir_pad_robot_count):
        robot_movement_table = calculate_dir_pad_table(robot_movement_table, i)
    robot_movement_table = calculate_num_pad_table(robot_movement_table, dir_pad_robot_count)

    # Add up the cost of transitioning to each next numpad key, and the cost of pressing each key.
    return sum(
        [robot_movement_table[(start_key, end_key)]
         for start_key, end_key
         in itertools.pairwise([AKey] + [AKey if key == "A" else int(key) for key in code])]
    ) + len(code)


def part1(input_data: InputType) -> ResultType:
    assert all([x.endswith("A") and x[:-1].isnumeric() for x in input_data])
    return sum([int(x[:-1]) * shortest_sequence(x, 2) for x in input_data])


def part2(input_data: InputType) -> ResultType:
    assert all([x.endswith("A") and x[:-1].isnumeric() for x in input_data])
    return sum([int(x[:-1]) * shortest_sequence(x, 25) for x in input_data])
