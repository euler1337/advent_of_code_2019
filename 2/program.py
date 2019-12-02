#!/usr/bin/env python3

PROGRAM_START_ADDRESS=0
OUTPUT_ADDRESS = 0
NOUN_ADDRESS=1
VERB_ADDRESS=2

PROGRAM_STEP_LENGTH=4

PROGRAM_ADD_CODE=1
PROGRAM_MULT_CODE=2
PROGRAM_STOP_CODE=99

KNOWN_OPERATOR_CODES = [PROGRAM_ADD_CODE, PROGRAM_MULT_CODE]


def pre_process(noun, verb, input_data):
    input_data[NOUN_ADDRESS] = noun
    input_data[VERB_ADDRESS] = verb
    return input_data

def run_instruction(program, address):
    op_code = program[address]
    val1_address = program[address+1]
    val1 = program[val1_address]
    val2_address = program[address+2]
    val2 = program[val2_address]
    destination = program[address+3]

    if op_code is PROGRAM_ADD_CODE:
        value = val1 + val2
        program[destination] = value
    elif op_code is PROGRAM_MULT_CODE:
        value = val1 * val2
        program[destination] = value
    else:
        raise RuntimeError("op_code: {} is not a supported operation".format(op_code))
    
    return program

def run_program(program):
    step_count = 0

    while(True):
        instruction_address = step_count * PROGRAM_STEP_LENGTH
        op_code = program[instruction_address]
        if op_code in KNOWN_OPERATOR_CODES:
            program = run_instruction(program, instruction_address) 
            step_count = step_count + 1
        elif op_code is PROGRAM_STOP_CODE:
            break
        else:
            raise RuntimeError("Do not recognize instruction with code: {}".format(op_code))
            
    return program



def a(input_data):
    NOUN_VALUE = 12
    VERB_VALUE = 2
    data = pre_process(NOUN_VALUE, VERB_VALUE, input_data)
    output_program = run_program(data)
    print("A, answer is: {}".format(output_program[OUTPUT_ADDRESS]))

def b(input_data):
    DESIRED_OUTPUT = 19690720
    program_length = len(input_data)

    for noun in range(program_length):
        for verb in range(program_length):
            data = pre_process(noun, verb, input_data.copy())
            output_program = run_program(data)
            if output_program[OUTPUT_ADDRESS] == DESIRED_OUTPUT:
                answer = 100*noun + verb
                print("B, answer: {}".format(answer)) 
                exit(0)


if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = f.readline().split(',')
    input_data = [int(x) for x in input_data]
    
    a(input_data.copy())
    b(input_data.copy())
    




