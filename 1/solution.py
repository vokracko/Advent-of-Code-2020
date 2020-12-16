#!/usr/bin/env python3

from itertools import combinations

numbers = [int(line) for line in open("input")]
results = [x*y for x, y in combinations(numbers, r=2) if x+y == 2020]
print(results)