#!/usr/bin/env python3

from pathlib import Path
import re
import sympy

class ClawMachine:
    def __init__(self, a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int]):
        self.a = a
        self.b = b
        self.prize = prize

    def __str__(self) -> str:
        return f"A:({self.a[0]},{self.a[1]}) B:({self.b[0]},{self.b[1]}) Prize:({self.prize[0]},{self.prize[1]})"

InputType = list[ClawMachine]
ResultType = int


def load(input_path: Path) -> InputType:
    machine_regex = re.compile("Button A: X\\+(?P<a_x>\\d+), Y\\+(?P<a_y>\\d+)\n" +
                               "Button B: X\\+(?P<b_x>\\d+), Y\\+(?P<b_y>\\d+)\n" +
                               "Prize: X=(?P<prize_x>\\d+), Y=(?P<prize_y>\\d+)")

    with open(input_path) as f:
        return [ClawMachine((int(m.group("a_x")), int(m.group("a_y"))),
                            (int(m.group("b_x")), int(m.group("b_y"))),
                            (int(m.group("prize_x")), int(m.group("prize_y")))) for m in
                [machine_regex.fullmatch(s) for s in f.read().strip().split("\n\n")]]


def part1(input_data: InputType) -> ResultType:
    result = 0

    for machine in input_data:
        # a_x * a_presses + bx * b_presses = prize_x
        # a_y * a_presses + by * b_presses = prize_y
        # Solve as a system of linear equations.

        m = sympy.Matrix([[machine.a[0], machine.b[0]], [machine.a[1], machine.b[1]]])
        p = sympy.Matrix([machine.prize[0], machine.prize[1]])
        solution = m.inv() * p
        if solution[0] % 1 != 0 or solution[1] % 1 != 0:
            continue
        if solution[0] > 100 or solution[1] > 100:
            continue
        result += 3 * solution[0] + solution[1]

    return result


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
