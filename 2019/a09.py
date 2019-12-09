""" Based on a071, does not incorporate a072 multi-process communication. """

import itertools
from collections import defaultdict
from contextlib import suppress
from functools import partial


def get_parameter(index, *, instruction_pointer, memory, parameter_modes, relative_base, write=False):
    mode = parameter_modes.get(index, 0)
    value = int(memory[instruction_pointer + index])
    if mode == 0:  # position mode
        if not write:
            value = memory[value]
    elif mode == 1:  # immediate mode
        if write:
            raise Exception("Cannot write to immediate mode address.")
    elif mode == 2:  # relative mode
        if not write:
            value = memory.get(relative_base + value, 0)
        else:
            value = relative_base + value
    else:
        raise Exception(f'wtf: {mode} is not a valid parameter mode')
    return int(value)


class Program:

    def __init__(self, program, inputs=None, debug=False):
        self.debug = debug
        self.outputs = []
        self.inputs = [val for val in inputs] if inputs else []
        self.read_program_to_memory(program)  # Sets memory and instruction_pointer
        self.relative_base = self.instruction_pointer

    def read_program_to_memory(self, program):
        if isinstance(program, str):
            program = program.strip().split(",")
        total_instructions = len(program)
        self.memory = defaultdict(int)
        for index, number in enumerate(program):
            self.memory[index] = number
        self.instruction_pointer = 0

    def log(self, message):
        if self.debug:
            print(message)

    @property
    def current_opcode(self):
        return self.memory[self.instruction_pointer]

    def run(self):
        while self.current_opcode != '99':
            self.log(f"Executing command {self.current_opcode} at {self.instruction_pointer}.")
            parameter_modes = defaultdict(int)
            if len(self.current_opcode) <= 2:
                opcode = int(self.current_opcode)
            else:
                opcode = int(self.current_opcode[-2:])
                for index, value in enumerate(self.current_opcode[:-2][::-1]):
                    parameter_modes[index + 1] = int(value)
            get_current_parameter = partial(
                get_parameter, instruction_pointer=self.instruction_pointer,
                memory=self.memory, parameter_modes=parameter_modes,
                relative_base=self.relative_base,
            )

            if opcode == 1:  # Addition
                instruction_length = 4
                parameter1 = get_current_parameter(1)
                parameter2 = get_current_parameter(2)
                parameter3 = get_current_parameter(3, write=True)
                self.memory[parameter3] = parameter1 + parameter2
                self.log(f"  Writing {parameter1} + {parameter2} = {self.memory[parameter3]} to {parameter3}")
            elif opcode == 2:  # Multiplication
                instruction_length = 4
                parameter1 = get_current_parameter(1)
                parameter2 = get_current_parameter(2)
                parameter3 = get_current_parameter(3, write=True)
                self.memory[parameter3] = parameter1 * parameter2
                self.log(f"  Writing {parameter1} * {parameter2} = {self.memory[parameter3]} to {parameter3}")
            elif opcode == 3:  # Input
                instruction_length = 2
                parameter1 = get_current_parameter(1, write=True)
                self.memory[parameter1] = self.inputs.pop(0)
                self.log(f"  Writing 1 to {parameter1}")
            elif opcode == 4:  # Output
                instruction_length = 2
                parameter1 = get_current_parameter(1)
                print("################### OUTPUT: " + str(parameter1))
                self.outputs.append(parameter1)
            elif opcode == 5:  # Jump if != 0
                instruction_length = 3
                parameter1 = get_current_parameter(1)
                parameter2 = get_current_parameter(2)
                if parameter1 != 0:
                    self.instruction_pointer = parameter2
                    self.log(f"  Setting instruction pointer to {parameter2} because {parameter1} != 0")
                    continue
            elif opcode == 6:  # Jump if == 0
                instruction_length = 3
                parameter1 = get_current_parameter(1)
                parameter2 = get_current_parameter(2)
                if parameter1 == 0:
                    self.instruction_pointer = parameter2
                    self.log(f"  Setting instruction pointer to {parameter2} because {parameter1} == 0")
                    continue
            elif opcode == 7:  # x < y
                instruction_length = 4
                parameter1 = get_current_parameter(1)
                parameter2 = get_current_parameter(2)
                parameter3 = get_current_parameter(3, write=True)
                self.memory[parameter3] = 1 if parameter1 < parameter2 else 0
                self.log(f"  Writing {self.memory[parameter3]} to {parameter3} because of {parameter1} < {parameter2}")
            elif opcode == 8:  # x == y
                instruction_length = 4
                parameter1 = get_current_parameter(1)
                parameter2 = get_current_parameter(2)
                parameter3 = get_current_parameter(3, write=True)
                self.memory[parameter3] = 1 if parameter1 == parameter2 else 0
                self.log(f"  Writing {self.memory[parameter3]} to {parameter3} because of {parameter1} == {parameter2}")
            elif opcode == 9:
                instruction_length = 2
                parameter1 = get_current_parameter(1)
                self.relative_base += parameter1
                self.log(f"  Setting relative_base to {self.relative_base} by adding {parameter1}")
            else:
                raise Exception("Invalid opcode: {}".format(opcode) + "\n\ndata: " + str(self.memory))
            self.instruction_pointer += instruction_length
        return self.memory, self.outputs
