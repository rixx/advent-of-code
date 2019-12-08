"""

The air conditioner comes online! Its cold air feels good for a while, but then
the TEST alarms start to go off. Since the air conditioner can't vent its heat
anywhere but back into the spacecraft, it's actually making the air inside the
ship warmer.

Instead, you'll need to use the TEST to extend the thermal radiators.
Fortunately, the diagnostic program (your puzzle input) is already equipped for
this. Unfortunately, your Intcode computer is not.

Your computer is only missing a few opcodes:

    Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.

Like all instructions, these instructions need to support parameter modes as
described above.

Normally, after an instruction is finished, the instruction pointer increases
by the number of values in that instruction. However, if the instruction
modifies the instruction pointer, that value is used and the instruction
pointer is not automatically increased.

For example, here are several programs that take one input, compare it to the
value 8, and then produce one output:

    3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
    3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
    3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
    3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).

Here are some jump tests that take an input, then output 0 if the input was
zero or 1 if the input was non-zero:

    3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
    3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)

Here's a larger example:

3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99

The above example program uses an input instruction to ask for a single number.
The program will then output 999 if the input value is below 8, output 1000 if
the input value is equal to 8, or output 1001 if the input value is greater
than 8.

This time, when the TEST diagnostic program runs its input instruction to get
the ID of the system to test, provide it 5, the ID for the ship's thermal
radiator controller. This diagnostic test suite only outputs one number, the
diagnostic code.

What is the diagnostic code for system ID 5?
"""
from collections import defaultdict
from functools import partial


def get_parameter(index, instruction_pointer, memory, parameter_modes):
    mode = parameter_modes.get(index, 'position')
    if mode == 'immediate':
        return memory[instruction_pointer + index]
    elif mode == 'position':
        return memory[int(memory[instruction_pointer + index])]
    raise Exception('wtf')


def run(program):
    if isinstance(program, str):
        program = program.strip().split(",")
    memory = {index: number for index, number in enumerate(program)}
    instruction_pointer = 0
    while int(memory[instruction_pointer]) != 99:
        print(f"Executing next command at {instruction_pointer}.")
        full_opcode = str(memory[instruction_pointer])   # Default 4-value instruction: opcode + 3 parameters
        print(f"  OPCODE {full_opcode}.")
        parameter_modes = defaultdict(lambda: 'position')
        if len(full_opcode) <= 2:
            opcode = int(full_opcode)
        else:
            opcode = int(full_opcode[-2:])
            for index, value in enumerate(full_opcode[:-2][::-1]):
                if int(value) == 1:
                    parameter_modes[index + 1] = 'immediate'
        get_current_parameter = partial(
            get_parameter, instruction_pointer=instruction_pointer,
            memory=memory, parameter_modes=parameter_modes,
        )
        if opcode == 1:
            instruction_length = 4
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            parameter3 = memory[instruction_pointer + 3]
            memory[int(parameter3)] = int(parameter1) + int(parameter2)
            print(f"  Writing {parameter1} + {parameter2} = {memory[int(parameter3)]} to {parameter3}")
        elif opcode == 2:
            instruction_length = 4
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            parameter3 = memory[instruction_pointer + 3]
            memory[int(parameter3)] = int(parameter1) * int(parameter2)
            print(f"  Writing {parameter1} * {parameter2} = {memory[int(parameter3)]} to {parameter3}")
        elif opcode == 3:
            instruction_length = 2
            parameter1 = memory[instruction_pointer + 1]
            magic_input = input("? ")
            memory[int(parameter1)] = magic_input
            print(f"  Writing 1 to {parameter1}")
        elif opcode == 4:
            instruction_length = 2
            parameter1 = get_current_parameter(1)
            # print("################### OUTPUT: " + str(memory[int(parameter1)]))  # TODO: modular output
            print("################### OUTPUT: " + str(parameter1))  # TODO: modular output
        elif opcode == 5:
            instruction_length = 3
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            if int(parameter1) != 0:
                instruction_pointer = int(parameter2)
                print(f"  Setting instruction pointer to {parameter2} because {parameter1} != 0")
                continue
        elif opcode == 6:
            instruction_length = 3
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            if int(parameter1) == 0:
                instruction_pointer = int(parameter2)
                print(f"  Setting instruction pointer to {parameter2} because {parameter1} == 0")
                continue
        elif opcode == 7:
            instruction_length = 4
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            parameter3 = memory[instruction_pointer + 3]
            memory[int(parameter3)] = 1 if int(parameter1) < int(parameter2) else 0
            print(f"  Writing {memory[int(parameter3)]} to {parameter3} because of {parameter1} < {parameter2}")
        elif opcode == 8:
            instruction_length = 4
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            parameter3 = memory[instruction_pointer + 3]
            memory[int(parameter3)] = 1 if int(parameter1) == int(parameter2) else 0
            print(f"  Writing {memory[int(parameter3)]} to {parameter3} because of {parameter1} == {parameter2}")
        else:
            raise Exception("invalid opcode: {}".format(opcode) + "\n\ndata: " + str(memory))
        instruction_pointer += instruction_length
    return memory
