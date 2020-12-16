#!/usr/bin/env python3

import re
from typing import Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class Policy:
    letter: str  # There is no "Char" type
    lower_bound: int
    upper_bound: int

    @classmethod
    def from_definition(cls, definition: str) -> None:
        match = re.search(
            r"(?P<lower_bound>\d+)-(?P<upper_bound>\d+) (?P<letter>[a-z])", definition
        )
        return cls(
            letter=match.group("letter"),
            lower_bound=int(match.group("lower_bound")),
            upper_bound=int(match.group("upper_bound")),
        )

    def allows(self, password: str):
        frequencies = Counter(password)
        letter_frequency = frequencies.get(self.letter, 0)
        return self.lower_bound <= letter_frequency <= self.upper_bound


def is_password_valid(line: str) -> Tuple[Policy, str]:
    policy_definition, password = line.split(":")
    policy = Policy.from_definition(policy_definition)
    return policy.allows(password.strip())


with open("input") as fd:
    results = [is_password_valid(line) for line in fd]
    print(sum(results))
