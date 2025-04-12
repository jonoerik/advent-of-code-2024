#!/usr/bin/env python3

from enum import Enum
import itertools
from pathlib import Path
import re

# ((register_a, register_b, register_c), [program])
InputType = tuple[tuple[int, int, int], list[int]]
ResultType = str


def load(input_path: Path) -> InputType:
    input_regex = re.compile("Register A: (?P<reg_a>\\d+)\n" +
                             "Register B: (?P<reg_b>\\d+)\n" +
                             "Register C: (?P<reg_c>\\d+)\n\n" +
                             "Program: (?P<prog>\\d+(?:,\\d+)*)")

    with (open(input_path) as f):
        match = input_regex.fullmatch(f.read().strip())
        return ((int(match.group("reg_a")), int(match.group("reg_b")), int(match.group("reg_c"))),
                [int(x) for x in match.group("prog").split(",")])


class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


def part1(input_data: InputType) -> ResultType:
    regs = list(input_data[0])
    output = []
    program = input_data[1]
    program_counter = 0

    # Print program assembly.
    # print("\n".join([f"{Opcode(a).name} {b if b < 4 else "*" + "ABC"[b-4]}" for a, b in itertools.batched(program, 2)]))

    while program_counter < len(input_data[1]):
        match Opcode(program[program_counter]), program[program_counter + 1]:
            case Opcode.ADV, operand if operand in range(4):
                regs[0] >>= operand
            case Opcode.ADV, reg if reg in range(4, 7):
                regs[0] >>= regs[reg-4]
            case Opcode.BXL, operand:
                regs[1] ^= operand
            case Opcode.BST, operand if operand in range(4):
                regs[1] = operand % 8
            case Opcode.BST, reg if reg in range(4, 7):
                regs[1] = regs[reg-4] % 8
            case Opcode.JNZ, operand:
                if regs[0] != 0:
                    program_counter = operand
                    continue
            case Opcode.BXC, _:
                regs[1] ^= regs[2]
            case Opcode.OUT, operand if operand in range(4):
                output.append(operand % 8)
            case Opcode.OUT, reg if reg in range(4, 7):
                output.append(regs[reg-4] % 8)
            case Opcode.BDV, operand if operand in range(4):
                regs[1] = regs[0] >> operand
            case Opcode.BDV, reg if reg in range(4, 7):
                regs[1] = regs[0] >> regs[reg-4]
            case Opcode.CDV, operand if operand in range(4):
                regs[2] = regs[0] >> operand
            case Opcode.CDV, reg if reg in range(4, 7):
                regs[2] = regs[0] >> regs[reg-4]
            case Opcode.ADV | Opcode.BST | Opcode.OUT | Opcode.BDV | Opcode.CDV, 7:
                # Invalid combo operand.
                assert False
            case _:
                assert False
        program_counter += 2

    return ",".join([str(x) for x in output])

def part2(input_data: InputType) -> ResultType:
    pass  # TODO
