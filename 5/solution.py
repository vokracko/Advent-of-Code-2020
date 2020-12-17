#!/usr/bin/env python3

from math import ceil
from dataclasses import dataclass
from itertools import product
from typing import Set, Tuple


class PositionDecoder:
    SELECT_LOWER: str
    SELECT_UPPER: str
    lower_bound: int = 0
    upper_bound: int

    def decode(self, control_sequence: str) -> int:
        control_character = control_sequence[0]
        distance = self.upper_bound - self.lower_bound

        if distance == 1:
            return (
                self.upper_bound
                if control_character is self.SELECT_UPPER
                else self.lower_bound
            )

        midpoint = distance / 2
        self.adjust_bounds(midpoint, control_character)
        return self.decode(control_sequence[1:])

    def adjust_bounds(self, midpoint: float, control_character: str):
        if control_character is self.SELECT_LOWER:
            self.upper_bound -= round(midpoint)
        elif control_character is self.SELECT_UPPER:
            self.lower_bound += ceil(midpoint)
        else:
            raise ValueError(f"Unexpected control character `{control_character}`")


class RowDecoder(PositionDecoder):
    SELECT_UPPER = "B"
    SELECT_LOWER = "F"
    upper_bound = 127


class ColumnDecoder(PositionDecoder):
    SELECT_UPPER = "R"
    SELECT_LOWER = "L"
    upper_bound = 7


def decode_seat_number(value: str) -> Tuple[int, int]:
    row_sequence, column_sequence = value[:7], value[7:]
    row = RowDecoder().decode(row_sequence)
    column = ColumnDecoder().decode(column_sequence)
    return row, column


def calculate_seat_id(row: int, column: int) -> int:
    return row * 8 + column


def get_my_seat_id(
    occupied_seat_numbers: Set[Tuple[int, int]], occupied_seat_ids: Set[int]
) -> int:
    all_seat_numbers = set(
        product(
            range(RowDecoder.lower_bound, RowDecoder.upper_bound + 1),
            range(ColumnDecoder.lower_bound, ColumnDecoder.upper_bound + 1),
        )
    )
    empty_or_missing_seats = all_seat_numbers - occupied_seat_numbers

    for row, column in empty_or_missing_seats:
        seat_id = calculate_seat_id(row, column)

        if all([seat_id - 1 in occupied_seat_ids, seat_id + 1 in occupied_seat_ids,]):
            return seat_id


occupied_seat_numbers = {
    decode_seat_number(line) for line in open("input").read().split("\n")
}
occupied_seat_ids = {
    calculate_seat_id(row, column) for row, column in occupied_seat_numbers
}
print("part one:", max(occupied_seat_ids))
print("part two:", get_my_seat_id(occupied_seat_numbers, occupied_seat_ids))
