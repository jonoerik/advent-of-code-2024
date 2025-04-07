#!/usr/bin/env python3

import math
from pathlib import Path
import re

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


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
