import itertools
from collections import defaultdict
from functools import partial


def get_parameter(index, instruction_pointer, memory, parameter_modes):
    mode = parameter_modes.get(index, 'position')
    if mode == 'immediate':
        return memory[instruction_pointer + index]
    elif mode == 'position':
        return memory[int(memory[instruction_pointer + index])]
    raise Exception('wtf')


def run(program, inputs, debug=False):
    outputs = []
    inputs = [val for val in inputs]
    if isinstance(program, str):
        program = program.strip().split(",")
    memory = {index: number for index, number in enumerate(program)}
    instruction_pointer = 0
    while int(memory[instruction_pointer]) != 99:
        if debug:
            print(f"Executing next command at {instruction_pointer}.")
        full_opcode = str(memory[instruction_pointer])   # Default 4-value instruction: opcode + 3 parameters
        if debug:
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
            if debug:
                print(f"  Writing {parameter1} + {parameter2} = {memory[int(parameter3)]} to {parameter3}")
        elif opcode == 2:
            instruction_length = 4
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            parameter3 = memory[instruction_pointer + 3]
            memory[int(parameter3)] = int(parameter1) * int(parameter2)
            if debug:
                print(f"  Writing {parameter1} * {parameter2} = {memory[int(parameter3)]} to {parameter3}")
        elif opcode == 3:
            instruction_length = 2
            parameter1 = memory[instruction_pointer + 1]
            memory[int(parameter1)] = inputs.pop(0)
            if debug:
                print(f"  Writing 1 to {parameter1}")
        elif opcode == 4:
            instruction_length = 2
            parameter1 = get_current_parameter(1)
            if debug:
                print("################### OUTPUT: " + str(parameter1))
            outputs.append(parameter1)
        elif opcode == 5:
            instruction_length = 3
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            if int(parameter1) != 0:
                instruction_pointer = int(parameter2)
                if debug:
                    print(f"  Setting instruction pointer to {parameter2} because {parameter1} != 0")
                continue
        elif opcode == 6:
            instruction_length = 3
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            if int(parameter1) == 0:
                instruction_pointer = int(parameter2)
                if debug:
                    print(f"  Setting instruction pointer to {parameter2} because {parameter1} == 0")
                continue
        elif opcode == 7:
            instruction_length = 4
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            parameter3 = memory[instruction_pointer + 3]
            memory[int(parameter3)] = 1 if int(parameter1) < int(parameter2) else 0
            if debug:
                print(f"  Writing {memory[int(parameter3)]} to {parameter3} because of {parameter1} < {parameter2}")
        elif opcode == 8:
            instruction_length = 4
            parameter1 = get_current_parameter(1)
            parameter2 = get_current_parameter(2)
            parameter3 = memory[instruction_pointer + 3]
            memory[int(parameter3)] = 1 if int(parameter1) == int(parameter2) else 0
            if debug:
                print(f"  Writing {memory[int(parameter3)]} to {parameter3} because of {parameter1} == {parameter2}")
        else:
            raise Exception("invalid opcode: {}".format(opcode) + "\n\ndata: " + str(memory))
        instruction_pointer += instruction_length
    return memory, outputs


def test_amplifier_settings(setting, program):
    result = []
    inputs = [setting[0], 0]
    for index in range(len(setting)):
        inputs[0] = setting[index]
        _, outputs = run(program, inputs, debug=False)
        inputs[1] = outputs[0]
    return inputs[1]


def get_max_setting(program):
    max_setting = None
    max_value = 0

    for setting in itertools.permutations('01234'):
        result = int(test_amplifier_settings(setting, program))
        if result > max_value:
            max_value = result
            max_setting = setting
    return max_setting, max_value
