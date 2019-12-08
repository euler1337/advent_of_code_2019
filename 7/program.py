#!/usr/bin/env python3

import copy
import queue

PROGRAM_START_ADDRESS=0
OUTPUT_ADDRESS = 0
NOUN_ADDRESS=1
VERB_ADDRESS=2

PROGRAM_STEP_LENGTH=4

PROGRAM_ADD_CODE=1
PROGRAM_MULT_CODE=2
PROGRAM_INPUT_CODE=3
PROGRAM_OUTPUT_CODE=4

PROGRAM_JUMP_TRUE_CODE=5
PROGRAM_JUMP_FALSE_CODE=6
PROGRAM_LESS_THAN_CODE=7
PROGRAM_EQUALS_CODE=8

PROGRAM_STOP_CODE=99

KNOWN_OPERATOR_CODES = [PROGRAM_ADD_CODE, 
                        PROGRAM_MULT_CODE, 
                        PROGRAM_INPUT_CODE, 
                        PROGRAM_OUTPUT_CODE,
                        PROGRAM_JUMP_TRUE_CODE,
                        PROGRAM_JUMP_FALSE_CODE,
                        PROGRAM_LESS_THAN_CODE,
                        PROGRAM_EQUALS_CODE,
]

OPERATOR_NUMBER_OF_PARAMETERS = {
    PROGRAM_ADD_CODE : 3,
    PROGRAM_MULT_CODE : 3,
    PROGRAM_INPUT_CODE : 1,
    PROGRAM_OUTPUT_CODE : 1,
    PROGRAM_JUMP_TRUE_CODE : 2,
    PROGRAM_JUMP_FALSE_CODE : 2,
    PROGRAM_LESS_THAN_CODE : 3,
    PROGRAM_EQUALS_CODE : 3,
    PROGRAM_STOP_CODE : 0
    }


PROGRAM_OUTPUT_QUEUE = queue.Queue()
PROGRAM_INPUT_QUEUE = queue.Queue()

NON_INTERACTIVE_MODE = 'NON_INTERACTIVE'
INTERACTIVE_MODE = 'INTERACTIVE'

def reverse_string(string):
    return string[len(string)::-1]

def get_address_pointer_increment(op_code):
    return OPERATOR_NUMBER_OF_PARAMETERS[int(op_code)] + 1

def parse_instruction(program, address_pointer):
    data = reverse_string(str(program[address_pointer]))

    op_code = int(reverse_string(data[:2]))
    parameter_modes = [0] * OPERATOR_NUMBER_OF_PARAMETERS[op_code]
    for index, x in enumerate(data[2:]):
        parameter_modes[index] = x

    return op_code, parameter_modes

def is_positional(parameter_mode):
    return int(parameter_mode) == 0

def is_immediate(parameter_mode):
    return int(parameter_mode) == 1


def get_parameter_value(parameter_modes, parameter_index, program, address_pointer):
    ''' parameter_index is 1, 2, 3, ...'''
    if is_positional(parameter_modes[parameter_index-1]):
        val = get_positional_value(program, address_pointer+parameter_index)
    elif is_immediate(parameter_modes[parameter_index-1]):
        val = get_immediate_value(program, address_pointer+parameter_index)
    else:
        raise RuntimeError("parameter mode is not recognized: {}".format(parameter_modes[parameter_index-1]))
    return int(val)

def get_positional_value(program, address):
    target_address = program[address]
    return program[target_address]

def get_immediate_value(program, address):
    return program[address]

def set_program_output(item):
    PROGRAM_OUTPUT_QUEUE.put(item)

def get_program_output():
    if PROGRAM_OUTPUT_QUEUE.empty():
        raise(RuntimeError("Output Queue is empty"))
    return PROGRAM_OUTPUT_QUEUE.get()

def add_program_input(item):
    return PROGRAM_INPUT_QUEUE.put(item)

def get_program_input():
    if PROGRAM_INPUT_QUEUE.empty():
        raise(RuntimeError("Input Queue is empty"))
    return PROGRAM_INPUT_QUEUE.get()

def clear_program_input():
    PROGRAM_INPUT_QUEUE.queue.clear()

def run_instruction(program, address_pointer, op_code, parameter_modes, mode):

    output_written = False

    if op_code is PROGRAM_ADD_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)
        value = val1 + val2
        destination = program[address_pointer+3]
        program[destination] = value
        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_MULT_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)
        value = val1 * val2
        destination = program[address_pointer+3]
        program[destination] = value
        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_INPUT_CODE:
        destination = program[address_pointer+1]
        if mode == NON_INTERACTIVE_MODE:  
            input_data = get_program_input()
        elif mode == INTERACTIVE_MODE: 
            input_data = input("Enter your input value : ")
        else:
            raise(RuntimeError("DID NOT RECOGNIZE MODE: {}".format(mode)))
            
        program[destination] = input_data 
        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_OUTPUT_CODE:
        destination = program[address_pointer+1]
        #print("OPCODE_4: Value={}".format(program[destination]))
        set_program_output(program[destination])
        address_pointer = address_pointer + get_address_pointer_increment(op_code)
        output_written = True

    elif op_code is PROGRAM_JUMP_TRUE_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)
        if val1 > 0: 
            address_pointer = val2
        else:
            address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_JUMP_FALSE_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)
        if val1 == 0: 
            address_pointer = val2
        else:
            address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_LESS_THAN_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)

        destination = program[address_pointer+3]
            
        if val1 < val2:
            program[destination] = 1
        else:
            program[destination] = 0
        
        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_EQUALS_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)

        destination = program[address_pointer+3]
            
        if val1 == val2:
            program[destination] = 1
        else:
            program[destination] = 0

        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    else:
        raise RuntimeError("op_code: {} is not a supported operation".format(op_code))
    
    return program, address_pointer, output_written

def run_program(program, mode, address_pointer=0):
    done = False
    while(True):
        op_code, parameter_modes = parse_instruction(program, address_pointer)
        if op_code in KNOWN_OPERATOR_CODES:
            program, address_pointer, output_written = run_instruction(program, address_pointer, op_code, parameter_modes, mode) 
            if output_written:
                break
        elif op_code is PROGRAM_STOP_CODE:
            done = True
            break
        else:
            raise RuntimeError("Do not recognize instruction with code: {}, knows codes are {}".format(op_code, KNOWN_OPERATOR_CODES))
            
    return program, done, address_pointer


def run_program_amplifier(program, phase, input_signal):

    for x in phase:
        add_program_input(x)
        add_program_input(input_signal)
        run_program(program.copy(), NON_INTERACTIVE_MODE)
        input_signal = get_program_output()
    
    return input_signal

def a(input_data):
    # First input = phase setting
    # Second input = input signal (output from previous program)

    max_throttle = 0
    start_input = 0
    for num in range(0,43211):
        x_list = [int(x) for x in str(num)]
        if len(x_list) == 4:
            x_list.append(0)

        if 0 in x_list and 1 in x_list and 2 in x_list and 3 in x_list and 4 in x_list:
            phase = x_list
            output = run_program_amplifier(input_data.copy(), phase, start_input)
            max_throttle = max(max_throttle, output)

    print("A, answer={}".format(max_throttle))

def run_feedback_program_amplifier(program, phase, input_signal):
    programs = [program.copy(), program.copy(), program.copy(), program.copy(), program.copy()]
    address_pointers = [0,0,0,0,0]
    first_run = True
    done = False

    print("SUM={}".format(sum([sum(x) for x in programs])))
    while not done:
        for index, program in enumerate(programs):
            if first_run:
                add_program_input(phase[index])

            add_program_input(input_signal)
            programs[index], done, address_pointers[index] = run_program(program, NON_INTERACTIVE_MODE, address_pointers[index])
            if not done:
                output = get_program_output()
                input_signal = output
        
        first_run = False
    
    return output

def b(input_data):
    max_throttle = 0
    start_input = 0
    for num in range(0,98766):
        clear_program_input()
        x_list = [int(x) for x in str(num)]
        if len(x_list) == 4:
            x_list.append(0)

        if 5 in x_list and 6 in x_list and 7 in x_list and 8 in x_list and 9 in x_list:
            phase = x_list
            output = run_feedback_program_amplifier(input_data, phase, start_input)
            max_throttle = max(max_throttle, output)
            print("candidate, output={}, phase={}".format(output, phase))
            
    print("A, answer={}".format(max_throttle))

if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = f.readline().split(',')
    input_data = [int(x) for x in input_data]
    
    a(input_data.copy())
    b(input_data.copy())
    




