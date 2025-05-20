#!/usr/bin/env python3

from enum import Enum
import itertools
from pathlib import Path
import re
from typing import Generator


class Gate(Enum):
    AND = 0
    OR = 1
    XOR = 2

WireInitType = dict[str, bool]
# {(gate_type, input1, input2, output)}
GateSetType = set[tuple[Gate, str, str, str]]
InputType = tuple[WireInitType, GateSetType]
ResultType1 = int
ResultType2 = str


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


def part1(input_data: InputType) -> ResultType1:
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


def part2(input_data: InputType, num_gate_swaps = 4, expected_result ="sum") -> ResultType2:
    wire_init, gates = input_data

    match expected_result:
        case "and":
            assert all(g == Gate.AND and i1.startswith("x") and i2.startswith("y") and o.startswith("z") for
                       g, i1, i2, o in gates)
            swapped_gates = list(sorted((o for _, i1, i2, o in gates if i1[1:] != o[1:])))
            assert len(swapped_gates) == num_gate_swaps * 2
            return ",".join(swapped_gates)

        case "sum":
            def print_dot_diagram() -> None:
                """Output the contents of a Graphviz dot file showing the gates and connections.
                Helpful for visually identifying patterns in the input."""

                print("strict digraph {")

                for wire in wire_init.keys():
                    if wire.startswith("x") or wire.startswith("y"):
                        print(f"init_{wire} [shape=circle fillcolor=\"skyblue\""
                              f"style=\"filled\" label=\"{wire}\"]")

                max_z = max((int(o[1:]) for g, i1, i2, o in gates if o.startswith("z")))
                print(f"""end_z [shape=plaintext label=
                    <<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" BGCOLOR=\"palegreen\">
                    <TR>{"".join([f"<TD port=\"{i}\">{i}</TD>" for i in reversed(range(max_z + 1))])}</TR>
                    <TR><TD colspan=\"{max_z + 1}\">z</TD></TR></TABLE>>];""")

                for g, i1, i2, o in gates:
                    print(f"gate_{g.name}_{i1}_{i2}_{o} [label=\"{g.name}\n\n{o}\""
                          f" shape=\"{ {Gate.AND: "invtrapezium",
                                        Gate.OR: "invtriangle",
                                        Gate.XOR: "invhouse"}[g]}\""
                          f" fillcolor=\"{ {Gate.AND: "peachpuff",
                                            Gate.OR: "pink",
                                            Gate.XOR: "hotpink"}[g]}\""
                          f" style=\"filled\"];")

                for g, i1, i2, o in gates:
                    if i1.startswith("x") or i1.startswith("y"):
                        print(f"init_{i1}:s -> gate_{g.name}_{i1}_{i2}_{o}:ne;")
                    if i2.startswith("x") or i2.startswith("y"):
                        print(f"init_{i2}:s -> gate_{g.name}_{i1}_{i2}_{o}:nw;")
                    if o.startswith("z"):
                        print(f"gate_{g.name}_{i1}_{i2}_{o}:s -> end_z:{int(o[1:])}:n;")
                for (g1, i11, i12, o1), (g2, i21, i22, o2) in itertools.product(gates, repeat=2):
                    if o1 == i21:
                        print(f"gate_{g1.name}_{i11}_{i12}_{o1}:s -> gate_{g2.name}_{i21}_{i22}_{o2}:ne;")
                    if o1 == i22:
                        print(f"gate_{g1.name}_{i11}_{i12}_{o1}:s -> gate_{g2.name}_{i21}_{i22}_{o2}:nw;")

                print("}")

            #print_dot_diagram()

            # The output diagram shows clear groups of 2 AND gates, 2 XOR gates, and a single OR gate; the building
            # blocks of a full adder.
            #
            # xnn ----o---+
            #         |   XOR--o--+
            # ynn --o-----+    |  XOR--- znn
            #       | |        |  |
            # Cnn -----------o----+
            #       | |      | |
            #       | |      +AND--+
            #       | |            OR--- C(nn + 1))
            #       +AND-----------+
            #
            # Label these gates, top to bottom:
            # - XOR_IN
            # - XOR_OUT
            # - AND_CARRY
            # - OR_CARRY
            # - AND_IN
            #
            # As we're adding 45-bit binary values, we have a total of 2 + ((45 - 1) * 5) gates; a full adder for each
            # input bit, except for bit 0 which only requires a 2 gate half adder.

            input_bits = max(int(w[1:]) for w in wire_init if w.startswith("x")) + 1
            assert input_bits == max(int(w[1:]) for w in wire_init if w.startswith("y")) + 1
            output_bits = max((int(o[1:]) for g, i1, i2, o in gates if o.startswith("z"))) + 1

            # As XOR_IN and AND_IN gates only have x and y wires as inputs, (and therefore can't have their inputs
            # swapped), we can unambiguously identify them without trialling different wire swaps.
            # Map the bit nn to the name of the wire that (xnn XOR ynn) or (xnn AND ynn) is output on.
            gates_xor_in: dict[int, str] = {}
            gates_and_in: dict[int, str] = {}
            for g, i1, i2, o in gates:
                if g in {Gate.XOR, Gate.AND} and (i1.startswith("x") or i1.startswith("y")):
                    assert i1[1:] == i2[1:]
                    assert i2.startswith("y") if i1.startswith("x") else i2.startswith("x")
                    if g == Gate.XOR:
                        gates_xor_in[int(i1[1:])] = o
                    else:
                        gates_and_in[int(i1[1:])] = o
            assert len(gates_xor_in) == input_bits
            assert len(gates_and_in) == input_bits

            incorrect_wires: set[str] = set()

            def find_next_gate_types(wire: str) -> tuple[Gate, ...]:
                result = [g for g, i1, i2, _ in gates if i1 == wire or i2 == wire]
                assert len(result) in range(3)
                return tuple(result)

            # Identify all incorrectly wired XOR gates, and their swap candidates.
            for g, i1, i2, o in gates:
                next_gates = tuple(sorted(find_next_gate_types(o), key=lambda x: x.value))
                if g == Gate.XOR:
                    if o in gates_xor_in.values():
                        if not (o.startswith("z") and int(o[1:]) == 0) and next_gates != (Gate.AND, Gate.XOR):
                            incorrect_wires.add(o)
                    else:
                        if not o.startswith("z"):
                            incorrect_wires.add(o)
                elif g == Gate.AND:
                    if o in gates_and_in.values():
                        if next_gates != (Gate.AND, Gate.XOR) and next_gates != (Gate.OR,):
                            incorrect_wires.add(o)
                    else:
                        if next_gates != (Gate.OR,):
                            incorrect_wires.add(o)
                elif g == Gate.OR:
                    if next_gates != (Gate.AND, Gate.XOR) and not (o.startswith("z") and int(o[1:]) == output_bits - 1):
                        incorrect_wires.add(o)
                else:
                    # Shouldn't have any other types of gates in the input.
                    assert False

            # Count number of incorrect wires still not accounted for.
            remaining_swapped_wires = num_gate_swaps * 2 - len(incorrect_wires)
            # Find all possible results that include incorrect_wires.
            swapped_wire_possibilities = (incorrect_wires | set(test_incorrect_set) for test_incorrect_set in
                                          itertools.combinations(
                                              (o for _, _, _, o in gates if o not in incorrect_wires),
                                              remaining_swapped_wires))

            def all_possible_pairs(xs: set[str]) -> Generator[set[tuple[str, str]], None, None]:
                """For an even length set of strings, generate all possible options for pairing up elements.

                e.g. {A B C D} has these options:
                (A B) (C D)
                (A C) (B D)
                (A D) (B C)
                """
                assert len(xs) % 2 == 0
                if len(xs) > 0:
                    a = next(iter(xs))
                    for b in (xs - {a}):
                        for other_pairs in all_possible_pairs(xs - {a, b}):
                            yield {(a, b)} | other_pairs
                else:
                    yield set()

            def test_swapped_circuit(sgs: GateSetType) -> bool:
                """For a given 'fixed' gate configuration sgs (Swapped Gates), test to see if it forms the expected
                adder circuit."""
                # Look up gates by their type and input wires, and provide their output wire.
                gate_lookup = {(g, frozenset({i1, i2})): o for g, i1, i2, o in sgs}
                try:
                    half_adder_xor = gate_lookup[(Gate.XOR, frozenset({"x00", "y00"}))]
                    half_adder_and = gate_lookup[(Gate.AND, frozenset({"x00", "y00"}))]
                    if half_adder_xor != "z00":
                        return False
                    carry_bits = [half_adder_and]
                    full_adder_xor_ins = []
                    full_adder_xor_outs = []
                    full_adder_and_carrys = []
                    full_adder_or_carrys = []
                    full_adder_and_ins = []
                    for bit in range(1, output_bits - 1):
                        full_adder_xor_ins.append(gate_lookup[(Gate.XOR, frozenset({f"x{bit:02}", f"y{bit:02}"}))])
                        full_adder_xor_outs.append(
                            gate_lookup[(Gate.XOR, frozenset({full_adder_xor_ins[-1], carry_bits[-1]}))])
                        if full_adder_xor_outs[-1] != f"z{bit:02}":
                            return False
                        full_adder_and_ins.append(
                            gate_lookup[(Gate.AND, frozenset({f"x{bit:02}", f"y{bit:02}"}))])
                        full_adder_and_carrys.append(
                            gate_lookup[(Gate.AND, frozenset({full_adder_xor_ins[-1], carry_bits[-1]}))])
                        full_adder_or_carrys.append(
                            gate_lookup[(Gate.OR, frozenset({full_adder_and_ins[-1], full_adder_and_carrys[-1]}))])
                        carry_bits.append(full_adder_or_carrys[-1])
                    if carry_bits[-1] != f"z{output_bits-1:02}":
                        return False

                except KeyError:
                    # Expected gate was not found in gate_lookup.
                    return False

                return True

            for swapped_wires_under_test in swapped_wire_possibilities:
                for swapped_pairs_under_test in all_possible_pairs(swapped_wires_under_test):
                    swaps = {a: b for x, y in swapped_pairs_under_test for a, b in ((x, y), (y, x))}
                    swapped_gates = {(g, i1, i2, swaps[o]) if o in swaps else (g, i1, i2, o) for g, i1, i2, o in gates}
                    if test_swapped_circuit(swapped_gates):
                        return ",".join(sorted(swapped_wires_under_test))

            # One of the above swapped_wires_under_test should have worked.
            assert False

        case _:
            assert False
