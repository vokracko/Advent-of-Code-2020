#!/usr/bin/env python3

import re
from typing import Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class Policy:
    letter: str  # There is no "Char" type
    first_index: int
    second_index: int

    @classmethod
    def from_definition(cls, definition: str) -> None:
        match = re.search(
            r"(?P<first_index>\d+)-(?P<second_index>\d+) (?P<letter>[a-z])", definition
        )
        return cls(
            letter=match.group("letter"),
            first_index=int(match.group("first_index")) - 1,
            second_index=int(match.group("second_index")) - 1,
        )

    def allows(self, password: str):
        first_match = password[self.first_index] == self.letter
        second_match = password[self.second_index] == self.letter
        return first_match ^ second_match


def is_password_valid(line: str) -> Tuple[Policy, str]:
    policy_definition, password = line.split(":")
    policy = Policy.from_definition(policy_definition)
    return policy.allows(password.strip())


with open("input") as fd:
    results = [is_password_valid(line) for line in fd]
    print(sum(results))
