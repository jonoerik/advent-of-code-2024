#!/usr/bin/env python3

import collections
import itertools
from pathlib import Path
from typing import Generator

InputType = list[int]
ResultType = int


def load(input_path: Path) -> InputType:
    with open(input_path) as f:
        return [int(line.strip()) for line in f.readlines()]


def secret_gen(initial_secret: int) -> Generator[int, None, None]:
    yield initial_secret
    s = initial_secret
    while True:
        s = ((s * 64) ^ s) & 0xFFFFFF
        s = ((s // 32) ^ s) & 0xFFFFFF
        s = ((s * 2048) ^ s) & 0xFFFFFF
        yield s


def part1(input_data: InputType) -> ResultType:
    return sum(next(itertools.islice(secret_gen(initial_secret), 2000, None)) for initial_secret in input_data)


def part2(input_data: InputType) -> ResultType:
    # Each price change is in the range [-9, 9], 19 possible values. Therefore, we have 19^4 different possibilities for
    # our 4-change-sequence. This is small enough to allow storage of all possibilities in memory.
    # We construct a dictionary of {4-change-sequence: number of bananas acquired}, scanning through each monkey's
    # price list in turn, and adding more bananas to the dictionary each time a sequence is seen for the first time
    # in that list. Then we can just select the largest result from the dictionary.

    banana_possibilities: dict[tuple[int, int, int, int], int] = collections.defaultdict(lambda: 0)

    for price_chain in ((x % 10 for x in secret_chain) for secret_chain in
                        (itertools.islice(secret_gen(initial_secret), 2001) for initial_secret in input_data)):
        sequences_not_yet_seen = set(itertools.product(range(-9, 10), repeat=4))

        last_price = next(price_chain)
        # Start with a dummy price difference value, which will be dropped before the first sequences_not_yet_seen check.
        price_differences = collections.deque([], 4)
        # Can't buy bananas at first 4 prices, as there hasn't been a long enough chain of price differences yet.
        for next_price in itertools.islice(price_chain, 3):
            price_differences.append(next_price - last_price)
            last_price = next_price

        for next_price in price_chain:
            price_differences.append(next_price - last_price)
            last_price = next_price
            if tuple(price_differences) in sequences_not_yet_seen:
                banana_possibilities[tuple(price_differences)] += next_price
                sequences_not_yet_seen.remove(tuple(price_differences))

    return max(banana_possibilities.values())
