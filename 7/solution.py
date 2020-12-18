#!/usr/bin/env python3

import re
from typing import DefaultDict, Dict, List, Tuple
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Bag:
    kind: str
    color: str

    @classmethod
    def from_definition(cls, line: str) -> Tuple["Bag", int]:
        match = re.match(r"^(?P<count>\d+ )?(?P<kind>\w+) (?P<color>\w+) bag", line)
        return (
            cls(kind=match.group("kind"), color=match.group("color")),
            int(match.group("count") or 0),
        )

    def __hash__(self) -> int:
        return hash(self.kind + self.color)


@dataclass
class Rule:
    parents: set = field(default_factory=set)
    children: list = field(default_factory=list)


class RuleSet:
    rules: DefaultDict[Bag, Rule]

    def __init__(self, rules: DefaultDict[Bag, Rule]) -> None:
        self.rules = rules

    def count_parents(self, bag: Bag, processed: set) -> int:
        total = 0

        for parent in self.rules[bag].parents:
            if parent not in processed:
                total += 1 + self.count_parents(parent, processed)
                processed.add(parent)

        return total

    def count_children(self, bag: Bag) -> int:
        return sum(
            [1 + self.count_children(child) for child in self.rules[bag].children]
        )

    @classmethod
    def from_file(cls, filename: str) -> "RuleSet":
        return cls.from_strings(open(filename).readlines())

    @classmethod
    def from_strings(cls, strings: List[str]) -> "RuleSet":
        rules: DefaultDict[Bag, Rule] = defaultdict(Rule)

        for rule in strings:
            bag_definition, contain_definition = rule.split("contain ")
            bag, _ = Bag.from_definition(bag_definition)

            if contain_definition == "no other bags.\n":
                continue

            for nested_bag_definition in contain_definition.split(", "):
                nested_bag, count = Bag.from_definition(nested_bag_definition)
                rules[nested_bag].parents.add(bag)
                rules[bag].children += [nested_bag] * count

        return cls(rules)


ruleset = RuleSet.from_file("input")
bag = Bag(kind="shiny", color="gold")
print("part one:", ruleset.count_parents(bag, set()))
print("part two:", ruleset.count_children(bag))
