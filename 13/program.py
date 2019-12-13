#!/usr/bin/env python3

import copy
import queue
from collections import namedtuple

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
PROGRAM_SET_RELATIVE_BASE_CODE=9

PROGRAM_STOP_CODE=99

KNOWN_OPERATOR_CODES = [PROGRAM_ADD_CODE, 
                        PROGRAM_MULT_CODE, 
                        PROGRAM_INPUT_CODE, 
                        PROGRAM_OUTPUT_CODE,
                        PROGRAM_JUMP_TRUE_CODE,
                        PROGRAM_JUMP_FALSE_CODE,
                        PROGRAM_LESS_THAN_CODE,
                        PROGRAM_EQUALS_CODE,
                        PROGRAM_SET_RELATIVE_BASE_CODE
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
    PROGRAM_STOP_CODE : 0,
    PROGRAM_SET_RELATIVE_BASE_CODE : 1
    }


PROGRAM_OUTPUT_QUEUE = queue.Queue()
PROGRAM_INPUT_QUEUE = queue.Queue()
PROGRAM_RELATIVE_BASE = {}
OUT_OF_RANGE_VALUES = {}

NON_INTERACTIVE_MODE = 'NON_INTERACTIVE'
INTERACTIVE_MODE = 'INTERACTIVE'

def reverse_string(string):
    return string[len(string)::-1]

def get_address_pointer_increment(op_code):
    return OPERATOR_NUMBER_OF_PARAMETERS[int(op_code)] + 1

def parse_instruction(program, address_pointer):
    data = reverse_string(str(read_data(program, address_pointer)))

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



def read_data(program, address):
    #print("READ data from address={}".format(address))
    if address >= len(program) :
        if address in OUT_OF_RANGE_VALUES:
            return OUT_OF_RANGE_VALUES[address]
        else:
            return 0
    else:
        return program[address]

def write_data(mode, program, address, value):
    
    if is_positional(mode):
        write_address = address
    elif is_relative(mode):
        write_address = address + get_relative_base()
    else:
        raise(RuntimeError("NON SUPPORTED WRITE MODE: {}".format(mode)))

    if write_address >= len(program) :
        OUT_OF_RANGE_VALUES[write_address] = value
    else:
        program[write_address] = value

    #print("Write value {} to address: {}, program: {}".format(value, write_address, program))
    
def get_positional_value(program, address):
    target_address = read_data(program, address)
    return read_data(program, target_address)

def get_immediate_value(program, address):
    return read_data(program, address)

def get_relative_value(program, address):
    relative_address = read_data(program, address) 
    target_address = relative_address + get_relative_base()
    
    #print("RELATIVE READ: Target-address={},relative-address={}, base={} value={}".format(target_address, relative_address,get_relative_base(),read_data(program, target_address)))
    return read_data(program, target_address)

def set_program_output(item):
    PROGRAM_OUTPUT_QUEUE.put(item)

def is_program_output_empty():
    return PROGRAM_OUTPUT_QUEUE.empty()

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
    PROGRAM_RELATIVE_BASE[program_name] = PROGRAM_RELATIVE_BASE[program_name] + value
    #print("SET RELATIVE BASE TO: {}".format(PROGRAM_RELATIVE_BASE[program_name]))

def get_relative_base(program_name = "default"):
    return PROGRAM_RELATIVE_BASE[program_name]

def run_instruction(program, address_pointer, op_code, parameter_modes, mode):

    output_written = False
    input_received = False

    #print("RUNNING INSTRUCTION: op_code={}".format(op_code))

    if op_code is PROGRAM_ADD_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)
        value = val1 + val2
        destination = read_data(program, address_pointer+3)
        write_data(parameter_modes[2], program, destination, value)
        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_MULT_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)
        value = val1 * val2
        destination = read_data(program, address_pointer+3)
        write_data(parameter_modes[2], program, destination, value)
        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_INPUT_CODE:
        #dest = get_parameter_value(parameter_modes, 1, program, address_pointer)
        destination = read_data(program, address_pointer+1)

        if mode == NON_INTERACTIVE_MODE:  
            input_data = get_program_input()
        elif mode == INTERACTIVE_MODE: 
            input_data = ''
            while len(input_data) == 0:
                input_data = input("Enter your input value : ")
                if input_data == "a":
                    input_data = "-1"
                elif input_data == "d":
                    input_data = "1"
        else:
            raise(RuntimeError("DID NOT RECOGNIZE MODE: {}".format(mode)))
            
        write_data(parameter_modes[0], program, destination, input_data) 
        address_pointer = address_pointer + get_address_pointer_increment(op_code)
        input_received = True

    elif op_code is PROGRAM_OUTPUT_CODE:
        output_value = get_parameter_value(parameter_modes, 1, program, address_pointer)
        set_program_output(output_value)
        #print("OUTPUT Value={}".format(output_value))
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

        destination = read_data(program, address_pointer+3)
            
        if val1 < val2:
            write_data(parameter_modes[2], program, destination, 1)
        else:
            write_data(parameter_modes[2], program, destination, 0)
        
        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_EQUALS_CODE:
        val1 = get_parameter_value(parameter_modes, 1, program, address_pointer)
        val2 = get_parameter_value(parameter_modes, 2, program, address_pointer)

        destination = read_data(program, address_pointer+3)
            
        if val1 == val2:
            write_data(parameter_modes[2], program, destination, 1)
        else:
            write_data(parameter_modes[2], program, destination, 0)

        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    elif op_code is PROGRAM_SET_RELATIVE_BASE_CODE:
        val = get_parameter_value(parameter_modes, 1, program, address_pointer)
        set_relative_base(val)
        address_pointer = address_pointer + get_address_pointer_increment(op_code)

    else:
        raise RuntimeError("op_code: {} is not a supported operation".format(op_code))
    
    return program, address_pointer, output_written, input_received

def run_program(program, mode, address_pointer=0):
    done = False
    while(True):
        op_code, parameter_modes = parse_instruction(program, address_pointer)
        if op_code in KNOWN_OPERATOR_CODES:
            program, address_pointer, output_written, input_received = run_instruction(program, address_pointer, op_code, parameter_modes, mode) 
            if input_received:
                break
        elif op_code is PROGRAM_STOP_CODE:
            done = True
            break
        else:
            raise RuntimeError("Do not recognize instruction with code: {}, knows codes are {}".format(op_code, KNOWN_OPERATOR_CODES))
            
    return program, done, address_pointer

Coordinate = namedtuple('Coordinate', 'x, y')
OUTPUT_MAP = {}
PROGRAM_DATA = {}

def parse_program_output():
    output = []

    while not is_program_output_empty():
        output.append(get_program_output())

    return output

def draw(tile, x, y):
    #print("Tile: {}, X: {}, Y:{}".format(tile, x, y))
    c = Coordinate(x,y)

    if x == -1 and y == 0:
        PROGRAM_DATA["score"] = tile
        print("SCORE: {}".format(tile))
    elif str(tile) in "01234":
        OUTPUT_MAP[c] = tile
    else:
        raise(RuntimeError("INVALID TILE: {}".format(tile)))

def parse_game(game_program):
    #0 is an empty tile. No game object appears in this tile.
    #1 is a wall tile. Walls are indestructible barriers.
    #2 is a block tile. Blocks can be broken by the ball.
    #3 is a horizontal paddle tile. The paddle is indestructible.
    #4 is a ball tile. The ball moves diagonally and bounces off objects.

    address_pointer = 0
    done = False
    x_max = 0
    y_max = 0
    print("Parsing program with length: {}".format(len(game_program)))
    while not done:
        x = game_program[address_pointer]
        y = game_program[address_pointer+1]
        tile = game_program[address_pointer+2]

        x_max = max(x_max,x)
        y_max = max(y_max,y)

        draw(tile, x, y)
        address_pointer = address_pointer + 3

        if address_pointer >= len(game_program) - 1:
            #print("Done parsing program: address_ptr: {}, program_len = {}".format(address_pointer, len(game_program)))
            done = True

    PROGRAM_DATA["x_max"] = max(PROGRAM_DATA["x_max"], x_max)
    PROGRAM_DATA["y_max"] = max(PROGRAM_DATA["y_max"], y_max)


def a(input_data):
    address_pointer = 0
    program = input_data
    done = False

    while not done:
        program, done, address_pointer = run_program(program, INTERACTIVE_MODE, address_pointer)
    game_program = parse_program_output()

    parse_game(game_program)

    tile_count = len([x for x in OUTPUT_MAP.values() if x == 2])
    print("A, answer: {}".format(tile_count))
        

def print_tile(tile):
    if tile == 0:
        return " "
    elif tile == 1:
        return "-"
    elif tile == 2:
        return "o"
    elif tile == 3:
        return "-"
    elif tile == 4:
        return "X"

def show_map():
    x_max = PROGRAM_DATA["x_max"]
    y_max = PROGRAM_DATA["y_max"]
    print("X_MAX: {}, Y_MAX: {}".format(x_max, y_max))
    matrix = [[" " for x in range(x_max+1)] for y in range(y_max+1)]
    # [y][x]

    for c, tile in OUTPUT_MAP.items():
        matrix[c.y][c.x] = print_tile(tile)
    
    #for y in range(y_max,-1,-1):
    for y in range(y_max):
        print("".join(matrix[y]))

def b(input_data):
    address_pointer = 0
    program = input_data
    done = False

    program[0] = 2
    PROGRAM_DATA["x_max"] = 0
    PROGRAM_DATA["y_max"] = 0


    while not done:
        program, done, address_pointer = run_program(program, INTERACTIVE_MODE, address_pointer)
        game_program = parse_program_output()
        parse_game(game_program)
        show_map()
        #OUTPUT_MAP.clear()

    print("GAME OVER: SCORE: {}".format(PROGRAM_DATA["score"]))

if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = f.readline().split(',')
    input_data = [int(x) for x in input_data]
    PROGRAM_RELATIVE_BASE["default"] = 0

    #a(input_data.copy())
    b(input_data.copy())
    




