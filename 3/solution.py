#!/usr/bin/env python3

from itertools import count
from functools import reduce
from operator import mul
from typing import Iterable, Tuple


class InfiniteString(str):
    def __getitem__(self, i: int) -> str:
        return super().__getitem__(i % len(self))


class Grid(list):
    def count_trees(self, coordinates: Iterable[Tuple[int, int]]) -> int:
        return sum([self.is_tree(row, column) for row, column in coordinates])

    def is_tree(self, row: int, column: int) -> bool:
        return self[row][column] == "#"

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as fd:
            return Grid([InfiniteString(line.strip()) for line in fd])


def generate_coordinates(down: int, right: int) -> Iterable[Tuple[int, int]]:
    return zip(range(down, len(grid), down), count(start=right, step=right))


grid = Grid.from_file("input")
coordinates = generate_coordinates(1, 3)
print("part one:", grid.count_trees(coordinates))

trees_encountered = []
for down, right in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
    coordinates = generate_coordinates(down, right)
    trees_encountered.append(grid.count_trees(coordinates))

print("part two:", reduce(mul, trees_encountered))
