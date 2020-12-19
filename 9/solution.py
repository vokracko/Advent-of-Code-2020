#!/usr/bin/env python3

from typing import List
from collections import deque
from itertools import permutations

preamble_size = 25
numbers = [int(line) for line in open("input").readlines()]


def get_first_invalid_number(numbers: List[int]) -> int:
    buffer = deque(numbers[:preamble_size], maxlen=preamble_size)

    for number in numbers[preamble_size:]:
        operands = [(x, y) for x, y in permutations(buffer, 2) if x + y == number]

        if not operands:
            return number

        buffer.append(number)


def get_weakness(numbers: List[int], target: int) -> int:
    for i in range(len(numbers)):
        for x in range(i + 1, len(numbers)):
            buffer = numbers[i:x]

            if sum(buffer) == target and len(buffer) >= 2:
                return max(buffer) + min(buffer)


target = get_first_invalid_number(numbers)
print("part one:", target)
print("part two:", get_weakness(numbers, target))
