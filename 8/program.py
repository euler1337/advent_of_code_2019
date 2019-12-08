#!/usr/bin/env python3

import copy
import queue

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

def a(input_data):
    number_of_layers =  int(len(input_data) / (IMAGE_WIDTH * IMAGE_HEIGHT))
    
    zero_count = []
    one_count = []
    two_count = []
    for index in range(0, number_of_layers):
        lower_limit = index * IMAGE_WIDTH * IMAGE_HEIGHT
        upper_limit = (index + 1) * IMAGE_WIDTH * IMAGE_HEIGHT
        layer_data = input_data[lower_limit : upper_limit]

        zero_count.append(layer_data.count(0))
        one_count.append(layer_data.count(1))
        two_count.append(layer_data.count(2))

    target_layer = zero_count.index(min(zero_count))

    print("A, answer: {}, ones: {}, twos: {}".format(one_count[target_layer] * two_count[target_layer], one_count[target_layer], two_count[target_layer]))

def b(input_data):
    print(input_data)

if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = f.readline()
    input_data = [int(x) for x in input_data]
    
    a(input_data.copy())
    #b(input_data.copy())
    




