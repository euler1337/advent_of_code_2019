#!/usr/bin/env python3

import math

def process_line_of_sight(source_x, source_y, target_x, target_y):
    vector = [target_x - source_x, target_y - source_y]

def to_key(x, y):
    return "{}_{}".format(x,y)

def dot_with_normal(x,y):
    x_1 = float(1)
    y_1 = float(0)

    x_2 = float(x)/(float(x) + float(y))
    y_2 = float(y)/(float(x) + float(y))

    return [x_1 * x_2, y_1 * y_2]
    

def a(input_data):

    line_of_sight_count = {}

    for source_y, source_row_data in enumerate(input_data):
        for source_x, source_item in enumerate(target_row_data):
            if source_item == '#':
                count = 0
                for target_y, target_row_data in enumerate(input_data):
                    for target_x, target_item in enumerate(target_row_data):
                        if target_item == '#':
                            add = process_line_of_sight(source_x, source_y, target_x, target_y)
                            if(add):
                                count = count + 1
            line_of_sight_count[to_key(source_x, source_y)] = count
    
    
    
    # Loop over grid
        # if asteroid
            # iterate over grid again
                # if asteroid
                    # sin and cos for angle between source and target.
                        # if not already in list, add to list, increase asteroid count.

def b(input_data):
    pass

        
if __name__ == '__main__':
    f = open("input2.txt", "r")
    input_data = [x.strip() for x in f.readlines()]

    print(dot_with_normal(2657,2424))

    #a(input_data.copy())
    #b(input_data.copy())
    




