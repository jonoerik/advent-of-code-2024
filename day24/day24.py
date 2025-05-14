#!/usr/bin/env python3

from enum import Enum
from pathlib import Path
import re


class Gate(Enum):
    AND = 0
    OR = 1
    XOR = 2

WireInitType = dict[str, bool]
# {(gate_type, input1, input2, output)}
GateSetType = set[tuple[Gate, str, str, str]]
InputType = tuple[WireInitType, GateSetType]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        inits: WireInitType = {}
        init_re = re.compile(r"(?P<name>\w+): (?P<val>[01])")
        while line := f.readline().strip():
            m = init_re.fullmatch(line)
            assert m
            inits[m.group("name")] = {"0": False, "1": True}[m.group("val")]

        gates: GateSetType = set()
        gate_re = re.compile(r"(?P<input1>\w+) (?P<gate>AND|OR|XOR) (?P<input2>\w+) -> (?P<output>\w+)")
        for line in f.readlines():
            line = line.strip()

            m = gate_re.fullmatch(line)
            assert m
            gates.add(({"AND": Gate.AND, "OR": Gate.OR, "XOR": Gate.XOR}[m.group("gate")],
                       m.group("input1"), m.group("input2"), m.group("output")))

        return inits, gates


def part1(input_data: InputType) -> ResultType:
    wire_init, gates = input_data
    wire_states: dict[str, bool | None] = {
        wire: wire_init[wire] if wire in wire_init else None
        for wire in set(wire_init.keys()) | set().union(*((input1, input2, output)
                                                          for _, input1, input2, output in gates))
    }

    while None in (v for k, v in wire_states.items() if k.startswith("z")):
        gate, input1, input2, output = next((g, i1, i2, out) for g, i1, i2, out in gates
                                            if wire_states[i1] is not None and wire_states[i2] is not None
                                            and wire_states[out] is None)
        wire_states[output] = {
            Gate.AND: wire_states[input1] and wire_states[input2],
            Gate.OR: wire_states[input1] or wire_states[input2],
            Gate.XOR: wire_states[input1] != wire_states[input2]
        }[gate]

    return sum(1 << int(wire[1:]) for wire in wire_states.keys() if wire.startswith("z") and wire_states[wire] == True)


def part2(input_data: InputType) -> ResultType:
    pass  # TODO
