#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import Tuple, List
from copy import deepcopy


class LoopDetected(Exception):
    ...


@dataclass
class Instruction:
    argument: int
    executions: int = 0

    def execute(self) -> Tuple[int, int]:
        if self.executions == 1:
            raise LoopDetected()

        self.executions += 1

    def __deepcopy__(self, *args) -> "Instruction":
        return type(self)(self.argument)


class Nop(Instruction):
    def execute(self) -> Tuple[int, int]:
        super().execute()
        return +1, 0

    def get_opposite(self) -> Instruction:
        return Jmp(self.argument)


class Jmp(Instruction):
    def execute(self) -> Tuple[int, int]:
        super().execute()
        return self.argument, 0

    def get_opposite(self) -> Instruction:
        return Nop(self.argument)


class Acc(Instruction):
    def execute(self) -> Tuple[int, int]:
        super().execute()
        return +1, self.argument


@dataclass
class Processor:
    instructions: List[Instruction]
    accumulator: int = 0
    position: int = 0

    def execute(self):
        while self.position != len(self.instructions):
            instruction = self.instructions[self.position]
            position_change, acc_change = instruction.execute()
            self.position += position_change
            self.accumulator += acc_change

    def execute_until_loop(self) -> int:
        try:
            self.execute()
        except LoopDetected:
            return self.accumulator

    def execute_corrections(self) -> int:
        for position, instruction in enumerate(self.instructions):
            if isinstance(instruction, (Nop, Jmp)):
                instructions = deepcopy(self.instructions)
                instructions[position] = instruction.get_opposite()
                try:
                    processor = Processor(instructions)
                    processor.execute()
                    return processor.accumulator
                except LoopDetected:
                    pass

    @classmethod
    def from_file(cls, filename: str) -> "Processor":
        return cls.from_string(open(filename).read())

    @classmethod
    def from_string(cls, string: str) -> "Processor":
        table = {
            "nop": Nop,
            "jmp": Jmp,
            "acc": Acc,
        }
        matches = re.findall(
            r"^(?P<command>\w+) (?P<argument>[+-]\d+)$", string, re.MULTILINE
        )
        instructions = [table[command](int(argument)) for command, argument in matches]
        return cls(instructions)


processor = Processor.from_file("input")
print("part one:", processor.execute_until_loop())
print("part two:", processor.execute_corrections())
