#!/usr/bin/env python3

import math
from pathlib import Path
import re
import statistics

class Robot:
    def __init__(self, p: tuple[int, int], v: tuple[int, int]):
        self.pos = p
        self.vel = v

    def __str__(self) -> str:
        return f"p={self.pos[0]},{self.pos[1]} v={self.vel[0]},{self.vel[1]}"

InputType = list[Robot]
ResultType = int


def load(input_path: Path) -> InputType:
    robot_regex = re.compile(r"p=(?P<px>\d+),(?P<py>\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)")

    with open(input_path) as f:
        return [Robot((int(match.group("px")), int(match.group("py"))),
                      (int(match.group("vx")), int(match.group("vy"))))
                for match in [robot_regex.fullmatch(line.strip()) for line in f.readlines()]]


def part1(input_data: InputType, area_width: int = 101, area_height: int = 103) -> ResultType:
    t = 100
    for r in input_data:
        r.pos = ((r.pos[0] + r.vel[0] * t) % area_width, (r.pos[1] + r.vel[1] * t) % area_height)
    assert area_width % 2 == 1 and area_height % 2 == 1
    quadrants = [(r.pos[0] < area_width // 2, r.pos[1] < area_height // 2) for r in input_data
                 if r.pos[0] != area_width // 2 and r.pos[1] != area_height // 2]
    return math.prod([quadrants.count(q) for q in [(False, False), (False, True), (True, False), (True, True)]])


def part2(input_data: InputType, area_width: int = 101, area_height: int = 103) -> ResultType:
    def robot_path_period(r: Robot) -> int:
        """Return the time it takes the robot to return to its starting position."""
        start = r.pos
        p = r.pos
        seconds = 0
        while True:
            p = ((p[0] + r.vel[0]) % area_width, (p[1] + r.vel[1]) % area_height)
            seconds += 1
            if p == start:
                return seconds

    # Find the time it takes the robots to all end up at their starting positions.
    all_robots_period = math.lcm(*[robot_path_period(r) for r in input_data])
    # In both the example and the puzzle input, all robots have the same period, which is therefore the overall period.
    # But we calculate the LCM, so that this will still work for sets of robots with different periods.

    def closeness_rating() -> float:
        """Return the average 'closeness' of robots to each other.

        First, calculate the 'closeness' of each tile that contains a robot; the fraction of surrounding tiles that
        also contain robots.
        e.g. 0.0 for a tile with a robot but with no adjacent robots, and 1.0 for a tile with a robot and completely
        surrounded by robots.
        This does not treat edge tiles as adjacent to the tiles on the other side of the area; no wrap-around.

        Return the average of all closeness values.
        Result will be 1.0 if the area has no unoccupied tiles, and 0.0 if no two robots are adjacent.

        Can be used as a measure of approximately how 'clumped together' the robots are."""

        # Set of all tiles occupied by at least one robot.
        filled_cells = set([r.pos for r in input_data])

        # A list of the neighbourhoods of all filled cells.
        neighbourhoods = [[(nx, ny) for nx, ny in [(x-1, y-1), (x, y-1), (x+1, y-1),
                                                   (x-1, y), (x+1, y),
                                                   (x-1, y+1), (x, y+1), (x+1, y+1)]
                           if 0 <= nx < area_width and 0 <= ny < area_height]
                          for x, y in filled_cells]

        return statistics.fmean([float(len([tile
                                            for tile in neighbourhood
                                            if tile in filled_cells]))
                                 / float(len(neighbourhood))
                                 for neighbourhood in neighbourhoods])

    best_closeness = 0.0
    best_closeness_t = None

    for t in range(all_robots_period):
        closeness = closeness_rating()
        if closeness > best_closeness:
            best_closeness = closeness
            best_closeness_t = t

            # Display robot layout:
            #print("\n" + "\n".join(["".join(["*" if (x, y) in [r.pos for r in input_data] else "."
            #                                 for x in range(area_width)]) for y in range(area_height)]))

        for robot in input_data:
            robot.pos = ((robot.pos[0] + robot.vel[0]) % area_width, (robot.pos[1] + robot.vel[1]) % area_height)

    return best_closeness_t
