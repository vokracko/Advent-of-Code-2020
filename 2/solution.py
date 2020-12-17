#!/usr/bin/env python3

import re
from typing import Type, Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class Policy:
    letter: str  # There is no "Char" type
    first: int
    second: int

    @classmethod
    def from_definition(cls, definition: str) -> "Policy":
        match = re.search(
            r"(?P<first>\d+)-(?P<second>\d+) (?P<letter>[a-z])", definition
        )
        return cls(
            letter=match.group("letter"),
            first=int(match.group("first")),
            second=int(match.group("second")),
        )

    def allows(self, password: str) -> bool:
        raise NotImplementedError


class FrequencyPolicy(Policy):
    def allows(self, password: str) -> bool:
        frequencies = Counter(password)
        letter_frequency = frequencies.get(self.letter, 0)
        return self.first <= letter_frequency <= self.second


class PositionPolicy(Policy):
    def allows(self, password: str) -> bool:
        first_match = password[self.first - 1] == self.letter
        second_match = password[self.second - 1] == self.letter
        return first_match ^ second_match


def is_password_allowed(line: str, policy: Type[Policy]) -> bool:
    policy_definition, password = line.split(":")
    return policy.from_definition(policy_definition).allows(password.strip())


lines = open("input").readlines()
print("part one:", sum([is_password_allowed(line, FrequencyPolicy) for line in lines]))
print("part two:", sum([is_password_allowed(line, PositionPolicy) for line in lines]))
