#!/usr/bin/env python3

import math

def get_angle_identifier(x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    cos_x = cosine(x,y)
    sin_x = sine(x,y)
    return "{}_{}".format(int(100000*cos_x), int(100000*sin_x))

def cosine(x,y):
    return dot_with_normal(x,y) / float(math.sqrt(math.pow(x,2) + math.pow(y,2)))

def sine(x,y):
    return cross_with_normal(x,y) / float(math.sqrt(math.pow(x,2) + math.pow(y,2)))

def to_key(x, y):
    return "{}_{}".format(x,y)

def cross_with_normal(x,y):
    x1 = float(1)
    y1 = float(0)

    return x1 * y - y1 * x

def dot_with_normal(x,y):
    x1 = float(1)
    y1 = float(0)

    return x1 * x + y1 * y

def is_same(x1, y1, x2, y2):
    return x1 == x2 and y1 == y2

def a(input_data):

    line_of_sight_count = {}

    for y1, source_row_data in enumerate(input_data):
        for x1, source_item in enumerate(source_row_data):
            if source_item == '#':
                count = 0
                angles_covered = {}
                for y2, target_row_data in enumerate(input_data):
                    for x2, target_item in enumerate(target_row_data):
                        if target_item == '#':
                            if not is_same(x1, y1, x2, y2):
                                sin_cos = get_angle_identifier(x1, y1, x2, y2)
                                if not sin_cos in angles_covered:
                                    count = count + 1
                                    angles_covered[sin_cos] = 1 # just something
                line_of_sight_count[to_key(x1, y1)] = count


    max_val = 0
    for key, value in line_of_sight_count.items():
        max_val = max(max_val, value)

    print("A, answer: {}".format(max_val))

def b(input_data):
    pass
        
if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = [x.strip() for x in f.readlines()]

    a(input_data.copy())
    #b(input_data.copy())
    




