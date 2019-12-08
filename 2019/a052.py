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


run("3,225,1,225,6,6,1100,1,238,225,104,0,101,71,150,224,101,-123,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,2,205,209,224,1001,224,-3403,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1101,55,24,224,1001,224,-79,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1,153,218,224,1001,224,-109,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1002,201,72,224,1001,224,-2088,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,70,29,225,102,5,214,224,101,-250,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,12,52,225,1101,60,71,225,1001,123,41,224,1001,224,-111,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1102,78,66,224,1001,224,-5148,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1101,29,77,225,1102,41,67,225,1102,83,32,225,1101,93,50,225,1102,53,49,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,677,224,1002,223,2,223,1005,224,329,101,1,223,223,7,677,677,224,1002,223,2,223,1005,224,344,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,404,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,419,101,1,223,223,1007,677,677,224,1002,223,2,223,1005,224,434,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,449,1001,223,1,223,1008,226,677,224,1002,223,2,223,1006,224,464,101,1,223,223,8,677,677,224,1002,223,2,223,1006,224,479,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,108,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,107,677,226,224,102,2,223,223,1005,224,584,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,599,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,614,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,1008,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1007,226,677,224,102,2,223,223,1005,224,659,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,674,101,1,223,223,4,223,99,226")
