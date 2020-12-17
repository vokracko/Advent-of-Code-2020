#!/usr/bin/env python3

import re
from typing import Optional
from dataclasses import dataclass


@dataclass
class Passport:
    birth_year: Optional[str] = None
    issue_year: Optional[str] = None
    expiration_year: Optional[str] = None
    height: Optional[str] = None
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    passport_id: Optional[str] = None
    country_id: Optional[str] = None

    @classmethod
    def from_string(cls, value: str) -> "Passport":
        matches = re.findall(r"(?P<key>[a-z]{3}):(?P<value>\S+)", value, re.MULTILINE)
        dictionary = dict(matches)
        return cls(
            birth_year=dictionary.get("byr"),
            issue_year=dictionary.get("iyr"),
            expiration_year=dictionary.get("eyr"),
            height=dictionary.get("hgt"),
            hair_color=dictionary.get("hcl"),
            eye_color=dictionary.get("ecl"),
            passport_id=dictionary.get("pid"),
            country_id=dictionary.get("cid"),
        )

    def has_required_fields(self) -> bool:
        return all(
            [
                self.birth_year,
                self.issue_year,
                self.expiration_year,
                self.height,
                self.hair_color,
                self.eye_color,
                self.passport_id,
            ]
        )

    def has_required_fields_valid(self) -> bool:
        if not self.has_required_fields():
            return False

        return all(
            [
                self.is_birth_year_valid(),
                self.is_issue_year_valid(),
                self.is_expiration_year_valid(),
                self.is_height_valid(),
                self.is_hair_color_valid(),
                self.is_eye_color_valid(),
                self.is_passport_id_valid(),
            ]
        )

    def is_birth_year_valid(self) -> bool:
        # four digits; at least 1920 and at most 2002
        return self.is_in_interval(self.birth_year, 1920, 2002)

    def is_issue_year_valid(self) -> bool:
        # four digits; at least 2010 and at most 2020
        return self.is_in_interval(self.issue_year, 2010, 2020)

    def is_expiration_year_valid(self) -> bool:
        # four digits; at least 2020 and at most 2030
        return self.is_in_interval(self.expiration_year, 2020, 2030)

    def is_height_valid(self) -> bool:
        # a number followed by either cm or in:
        # If cm, the number must be at least 150 and at most 193.
        # If in, the number must be at least 59 and at most 76.
        unit = self.height[-2:]
        height = self.height[:-2]

        if unit == "cm":
            return self.is_in_interval(height, 150, 193)
        elif unit == "in":
            return self.is_in_interval(height, 59, 76)

        return False

    def is_hair_color_valid(self) -> bool:
        # a # followed by exactly six characters 0-9 or a-f.
        return re.match(r"^#[0-9a-f]{6}$", self.hair_color)

    def is_eye_color_valid(self) -> bool:
        # exactly one of: amb blu brn gry grn hzl oth.
        return self.eye_color in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    def is_passport_id_valid(self) -> bool:
        # a nine-digit number, including leading zeroes.
        return re.match(r"^\d{9}$", self.passport_id)

    @staticmethod
    def is_in_interval(value: str, lower: int, upper: int) -> bool:
        if not Passport.has_n_digits(value, len(str(lower))):
            return False

        try:
            return lower <= int(value) <= upper
        except ValueError:
            return False

    @staticmethod
    def has_n_digits(value: str, n: int) -> bool:
        return re.match(rf"^\d{{{n}}}$", value)


passports_data = open("input").read().split("\n\n")
passports = [Passport.from_string(string) for string in passports_data]
print("part one:", sum([p.has_required_fields() for p in passports]))
print("part two:", sum([p.has_required_fields_valid() for p in passports]))
