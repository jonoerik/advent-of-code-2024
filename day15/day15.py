#!/usr/bin/env python3

from enum import Enum
from pathlib import Path

class MapTile(Enum):
    ROBOT = 0
    BOX = 1
    WALL = 2
    EMPTY = 3
    BOX_LEFT = 4
    BOX_RIGHT = 5

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

MapType = list[list[MapTile]]
InputType = tuple[MapType, list[Direction]]
ResultType = int


def load(input_path: Path) -> InputType:
    warehouse_map = []
    with open(input_path) as f:
        while True:
            line = f.readline()
            line = line.strip()
            if len(line) == 0:
                break

            warehouse_map.append([{"@": MapTile.ROBOT,
                                   "O": MapTile.BOX,
                                   "#": MapTile.WALL,
                                   ".": MapTile.EMPTY}[c]
                                  for c in line])

        directions = [{"^": Direction.UP,
                       ">": Direction.RIGHT,
                       "v": Direction.DOWN,
                       "<": Direction.LEFT}[c]
                      for line in f.readlines() for c in line.strip()]

    # Ensure warehouse has walls around edges.
    assert (all([warehouse_map[r][0] == MapTile.WALL
                and warehouse_map[r][len(warehouse_map[0])-1] == MapTile.WALL
                for r in range(len(warehouse_map))])
            and all([warehouse_map[0][c] == MapTile.WALL
                     and warehouse_map[len(warehouse_map)-1][c] == MapTile.WALL
                     for c in range(len(warehouse_map[0]))]))

    return warehouse_map, directions


def part1(input_data: InputType) -> ResultType:
    warehouse_map, directions = input_data
    robot_pos = [(r, c)
                 for r, row in enumerate(warehouse_map)
                 for c, tile in enumerate(row)
                 if tile == MapTile.ROBOT][0]
    warehouse_map[robot_pos[0]][robot_pos[1]] = MapTile.EMPTY

    for d in directions:
        dr, dc = {Direction.UP: (-1, 0),
                  Direction.RIGHT: (0, 1),
                  Direction.DOWN: (1, 0),
                  Direction.LEFT: (0, -1)}[d]
        target_pos = (robot_pos[0] + dr, robot_pos[1] + dc)
        target_tile = warehouse_map[target_pos[0]][target_pos[1]]
        if target_tile == MapTile.WALL:
            pass
        elif target_tile == MapTile.EMPTY:
            robot_pos = target_pos
        elif target_tile == MapTile.BOX:
            push_target = target_pos
            while warehouse_map[push_target[0]][push_target[1]] == MapTile.BOX:
                push_target = (push_target[0] + dr, push_target[1] + dc)
            if warehouse_map[push_target[0]][push_target[1]] == MapTile.EMPTY:
                warehouse_map[push_target[0]][push_target[1]] = MapTile.BOX
                warehouse_map[target_pos[0]][target_pos[1]] = MapTile.EMPTY
                robot_pos = target_pos

    # Print the final state of the warehouse.
    # print("\n".join(["".join(
    #     ["@" if (r, c) == robot_pos else {MapTile.EMPTY: ".", MapTile.WALL: "#", MapTile.BOX: "O"}[tile] for c, tile
    #      in enumerate(row)]) for r, row in enumerate(warehouse_map)]))

    return sum([100 * r + c
                for r, row in enumerate(warehouse_map)
                for c, tile in enumerate(row)
                if tile == MapTile.BOX])


def part2(input_data: InputType) -> ResultType:
    warehouse_map, directions = input_data
    robot_pos = [(r, c)
                 for r, row in enumerate(warehouse_map)
                 for c, tile in enumerate(row)
                 if tile == MapTile.ROBOT][0]
    warehouse_map[robot_pos[0]][robot_pos[1]] = MapTile.EMPTY
    # Expand warehouse map.
    robot_pos = (robot_pos[0], robot_pos[1] * 2)
    warehouse_map = [[new_tile for tile in row for new_tile in {
        MapTile.WALL: (MapTile.WALL, MapTile.WALL),
        MapTile.BOX: (MapTile.BOX_LEFT, MapTile.BOX_RIGHT),
        MapTile.EMPTY: (MapTile.EMPTY, MapTile.EMPTY)
    }[tile]] for row in warehouse_map]

    def can_push(d: Direction, r: int, c: int) -> bool:
        target_push_tile = warehouse_map[r][c]
        match target_push_tile, direction:
            case MapTile.WALL, _:
                return False
            case MapTile.EMPTY, _:
                return True
            case MapTile.BOX_LEFT, Direction.UP:
                return can_push(d, r - 1, c) and can_push(d, r - 1, c + 1)
            case MapTile.BOX_LEFT, Direction.RIGHT:
                return can_push(d, r, c + 2)
            case MapTile.BOX_LEFT, Direction.DOWN:
                return can_push(d, r + 1, c) and can_push(d, r + 1, c + 1)
            case MapTile.BOX_RIGHT, Direction.UP:
                return can_push(d, r - 1, c) and can_push(d, r - 1, c - 1)
            case MapTile.BOX_RIGHT, Direction.DOWN:
                return can_push(d, r + 1, c) and can_push(d, r + 1, c - 1)
            case MapTile.BOX_RIGHT, Direction.LEFT:
                return can_push(d, r, c - 2)
            case _:
                assert False

    def do_push(d: Direction, r: int, c: int):
        target_push_tile = warehouse_map[r][c]
        match target_push_tile, direction:
            case MapTile.EMPTY, _:
                pass
            case MapTile.BOX_LEFT, Direction.UP:
                do_push(d, r - 1, c)
                do_push(d, r - 1, c + 1)
                warehouse_map[r-1][c] = MapTile.BOX_LEFT
                warehouse_map[r-1][c+1] = MapTile.BOX_RIGHT
                warehouse_map[r][c] = MapTile.EMPTY
                warehouse_map[r][c+1] = MapTile.EMPTY
            case MapTile.BOX_LEFT, Direction.RIGHT:
                do_push(d, r, c + 2)
                warehouse_map[r][c+2] = MapTile.BOX_RIGHT
                warehouse_map[r][c+1] = MapTile.BOX_LEFT
                warehouse_map[r][c] = MapTile.EMPTY
            case MapTile.BOX_LEFT, Direction.DOWN:
                do_push(d, r + 1, c)
                do_push(d, r + 1, c + 1)
                warehouse_map[r+1][c] = MapTile.BOX_LEFT
                warehouse_map[r+1][c+1] = MapTile.BOX_RIGHT
                warehouse_map[r][c] = MapTile.EMPTY
                warehouse_map[r][c+1] = MapTile.EMPTY
            case MapTile.BOX_RIGHT, Direction.UP:
                do_push(d, r - 1, c)
                do_push(d, r - 1, c - 1)
                warehouse_map[r-1][c] = MapTile.BOX_RIGHT
                warehouse_map[r-1][c-1] = MapTile.BOX_LEFT
                warehouse_map[r][c] = MapTile.EMPTY
                warehouse_map[r][c-1] = MapTile.EMPTY
            case MapTile.BOX_RIGHT, Direction.DOWN:
                do_push(d, r + 1, c)
                do_push(d, r + 1, c - 1)
                warehouse_map[r+1][c] = MapTile.BOX_RIGHT
                warehouse_map[r+1][c-1] = MapTile.BOX_LEFT
                warehouse_map[r][c] = MapTile.EMPTY
                warehouse_map[r][c-1] = MapTile.EMPTY
            case MapTile.BOX_RIGHT, Direction.LEFT:
                do_push(d, r, c - 2)
                warehouse_map[r][c-2] = MapTile.BOX_LEFT
                warehouse_map[r][c-1] = MapTile.BOX_RIGHT
                warehouse_map[r][c] = MapTile.EMPTY
            case _:
                assert False

    for direction in directions:
        dr, dc = {Direction.UP: (-1, 0),
                  Direction.RIGHT: (0, 1),
                  Direction.DOWN: (1, 0),
                  Direction.LEFT: (0, -1)}[direction]
        target_pos = (robot_pos[0] + dr, robot_pos[1] + dc)
        target_tile = warehouse_map[target_pos[0]][target_pos[1]]
        if target_tile == MapTile.WALL:
            pass
        elif target_tile == MapTile.EMPTY:
            robot_pos = target_pos
        elif target_tile == MapTile.BOX_LEFT or target_tile == MapTile.BOX_RIGHT:
            if can_push(direction, *target_pos):
                do_push(direction, *target_pos)
                robot_pos = target_pos

    # Print the final state of the warehouse.
    # print("\n".join(["".join(["@" if (r, c) == robot_pos else
    #                           {MapTile.EMPTY: ".", MapTile.WALL: "#", MapTile.BOX_LEFT: "[", MapTile.BOX_RIGHT: "]"}[
    #                               tile] for c, tile in enumerate(row)]) for r, row in enumerate(warehouse_map)]))

    return sum([100 * r + c
                for r, row in enumerate(warehouse_map)
                for c, tile in enumerate(row)
                if tile == MapTile.BOX_LEFT])
