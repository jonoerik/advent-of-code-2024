#!/usr/bin/env python3

from enum import Enum
import itertools
from pathlib import Path
import re

# ((register_a, register_b, register_c), [program])
InputType = tuple[tuple[int, int, int], list[int]]
ResultType1 = str
ResultType2 = int


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


def part1(input_data: InputType) -> ResultType1:
    regs = list(input_data[0])
    output = []
    program = input_data[1]
    program_counter = 0

    # Print program assembly.
    def print_program():
        for opcode, operand in itertools.batched(program, 2):
            opcode = Opcode(opcode)
            if opcode in [Opcode.BXC]:
                print(opcode.name)
            elif opcode in [Opcode.BXL, Opcode.JNZ]:
                print(f"{opcode.name} {operand}")
            else:
                if operand in range(4, 7):
                    print(f"{opcode.name} *{'ABC'[operand-4]}")
                else:
                    print(f"{opcode.name} {operand}")
    # print_program()

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


def part2(input_data: InputType) -> ResultType2:
    regs = list(input_data[0])
    program = input_data[1]

    # The input that will cause a program to output itself is specific to each program, and must be figured out manually.
    match program, regs:
        case [0,3,5,4,3,0], _:  # sample2
            # ADV 3
            # OUT *A
            # JNZ 0
            #
            # while True:
            #     A >>= 3
            #     output(A % 8)
            #     if A == 0:
            #         break
            #
            # Program pulls 3 bits at a time off the bottom of register A, and outputs them.
            # The first 3 bits are skipped.
            vs = [x << ((n + 1) * 3) for n, x in enumerate(program)]
            return sum(vs)

        case [2,4,1,5,7,5,1,6,0,3,4,3,5,5,3,0], [_, 0, 0]:  # input
            # BST *A
            # BXL 5
            # CDV *B
            # BXL 6
            # ADV 3
            # BXC
            # OUT *B
            # JNZ 0
            #
            # while True:
            #     B = A % 8
            #     B ^= 5
            #     C = A >> B
            #     B ^= 6
            #     A >>= 3
            #     B ^= C
            #     output(B % 8)
            #     if A == 0:
            #         break
            #
            # while True:
            #     x = A & 0b111
            #     y = (A >> (x ^ 0b101)) & 0b111
            #     output.append(x ^ 0b11 ^ y)
            #     A >>= 3
            #     if A == 0:
            #         break
            def find_initial_a(current_a: int, remaining_program: list[int]) -> int | None:
                if not remaining_program:
                    return current_a
                current_a <<= 3
                options_low_bits = [low_bits for low_bits in range(8)
                                    if ((low_bits ^ 0b11 ^
                                         ((current_a | low_bits) >> (low_bits ^ 0b101)))
                                        & 0b111) == remaining_program[-1]]
                if not options_low_bits:
                    return None
                options_a = [next_a
                             for next_a
                             in [find_initial_a(current_a | low_bits, remaining_program[:-1])
                                 for low_bits
                                 in options_low_bits]
                             if next_a is not None]
                if not options_a:
                    return None
                return min(options_a)

            return find_initial_a(0, program)

        case _:
            assert False
