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
PROGRAM_RELATIVE_BASE = {}

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

def is_relative(parameter_mode):
    return int(parameter_mode) == 2

def get_parameter_value(parameter_modes, parameter_index, program, address_pointer):
    ''' parameter_index is 1, 2, 3, ...'''
    if is_positional(parameter_modes[parameter_index-1]):
        val = get_positional_value(program, address_pointer+parameter_index)
    elif is_immediate(parameter_modes[parameter_index-1]):
        val = get_immediate_value(program, address_pointer+parameter_index)
    elif is_relative(parameter_modes[parameter_index-1]):
        val = get_relative_value(program, address_pointer+parameter_index)
    else:
        raise RuntimeError("parameter mode is not recognized: {}".format(parameter_modes[parameter_index-1]))
    return int(val)

def get_positional_value(program, address):
    target_address = program[address]
    return program[target_address]

def get_immediate_value(program, address):
    return program[address]

def get_relative_value(program, address):
    target_address = program[address] + get_relative_base()
    return program[target_address]

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

def set_relative_base(value, program_name = "default"):
    PROGRAM_RELATIVE_BASE[program_name] = value

def get_relative_base(program_name = "default"):
    return PROGRAM_RELATIVE_BASE[program_name]

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

def a(input_data):
    # First input = phase setting
    # Second input = input signal (output from previous program)

    print(input_data)



def b(input_data):
    pass

if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = f.readline().split(',')
    input_data = [int(x) for x in input_data]
    
    a(input_data.copy())
    b(input_data.copy())
    




