#!/usr/bin/env python3

from itertools import combinations

numbers = [int(line) for line in open("input")]
print([x * y for x, y in combinations(numbers, r=2) if x + y == 2020])
print([x * y * z for x, y, z in combinations(numbers, r=3) if x + y + z == 2020])
