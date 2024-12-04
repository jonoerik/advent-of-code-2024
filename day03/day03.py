#!/usr/bin/env python3

from pathlib import Path
import re

InputType = str
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return f.read().strip()


def part1(input_data: InputType) -> ResultType:
    mul_regex = re.compile(r"mul\((?P<x>[0-9]{1,3}),(?P<y>[0-9]{1,3})\)", flags=re.DOTALL)
    return sum([int(re_match.group("x")) * int(re_match.group("y")) for re_match in mul_regex.finditer(input_data)])


def part2(input_data: InputType) -> ResultType:
    mul_regex = re.compile(r"don't\(\).*?(?:do\(\)|$)|mul\((?P<x>[0-9]{1,3}),(?P<y>[0-9]{1,3})\)", flags=re.DOTALL)
    return sum([int(re_match.group("x")) * int(re_match.group("y")) for re_match in mul_regex.finditer(input_data)
                if re_match.group("x") is not None])
