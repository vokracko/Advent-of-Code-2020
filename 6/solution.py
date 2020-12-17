#!/usr/bin/env python3

from collections import Counter
from typing import Callable, List


def count_unique_questions(group_answers: str) -> int:
    counter = Counter(group_answers)
    counter.pop("\n", None)
    return len(counter)


def count_common_questions(group_answers: str) -> int:
    counter = Counter(group_answers)
    member_count = counter.pop("\n", 0) + 1
    common_questions = [letter for letter in counter if counter[letter] == member_count]
    return len(common_questions)


class GroupCounter:
    def __init__(self, groups: List[str]) -> None:
        self.groups = groups

    def count(self, strategy: Callable) -> int:
        return sum([strategy(group_answers.strip()) for group_answers in groups])


groups = open("input").read().split("\n\n")
group_counter = GroupCounter(groups)
print("part one:", group_counter.count(count_unique_questions))
print("part two:", group_counter.count(count_common_questions))
