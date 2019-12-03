#!/usr/bin/env python3

import collections

Coordinate = collections.namedtuple('Coordinate', 'x y')

def get_all_horizontal_coords(start, end, visited_coords, step_count):

    if end.x < start.x:
        loop_range = range(start.x - 1, end.x - 1, -1)
    else:
        loop_range = range(start.x + 1, end.x + 1, 1)

    step_counter = step_count
    for x in loop_range:
        if Coordinate(x=x, y=start.y) not in visited_coords:
            visited_coords[Coordinate(x=x, y=start.y)] = step_counter
        step_counter = step_counter + 1

    return step_counter

def get_all_vertical_coords(start, end, visited_coords, step_count):

    if end.y < start.y:
        loop_range = range(start.y - 1, end.y - 1, -1)
    else:
        loop_range = range(start.y + 1, end.y + 1, 1)
        
    step_counter = step_count
    for y in loop_range:
        if Coordinate(x=start.x, y=y) not in visited_coords:
            visited_coords[Coordinate(x=start.x, y=y)] = step_counter
        step_counter = step_counter + 1

    return step_counter

def get_end_coordinate(start, new_segment):
    direction = new_segment[0]
    segement_length = int(new_segment[1:])

    if direction == 'R':
        end = Coordinate(x=start.x + segement_length, y=start.y)
    elif direction == 'L':
        end = Coordinate(x=start.x - segement_length, y=start.y)
    elif direction == 'U':
        end = Coordinate(x=start.x, y=start.y + segement_length)
    elif direction == 'D':
       end = Coordinate(x=start.x, y=start.y - segement_length)
    else:
        raise(IOError("Error parsing segment {}".format(new_segment)))

    return end


def get_segment_coordinates(start, end, visited_coords, step_count):
    if start.x == end.x:
        step_counter = get_all_vertical_coords(start, end, visited_coords, step_count)
    elif start.y == end.y:
        step_counter = get_all_horizontal_coords(start, end, visited_coords, step_count)

    return step_counter 

def get_trace(wire, start):
    step_count = 1

    visited_coords = {}
    for segment in wire:
        end = get_end_coordinate(start, segment)
        old_step_delta = step_count
        step_count = get_segment_coordinates(start, end, visited_coords, step_count)
        start = end
    
    return visited_coords

def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def a(input_data):
    start = Coordinate(x=0, y=0)
    wire_1 = input_data[0]
    wire_2 = input_data[1]

    wire_1_visited = get_trace(wire_1, start)
    wire_2_visited = get_trace(wire_2, start)

    both_visited = set(wire_1_visited.keys()).intersection(set(wire_2_visited.keys()))
    sorted_visited = sorted(both_visited, key = lambda coord: manhattan_distance(start, coord))

    step_per_intersection = []
    for coord in both_visited:
        step_per_intersection.append(wire_1_visited[coord] + wire_2_visited[coord])

    print("A, answer: {}".format(manhattan_distance(start, sorted_visited[0])))
    print("B, answer: {}".format(min(step_per_intersection)))


if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = [x.split(',') for x in f.readlines()]
    
    a(input_data)
    




