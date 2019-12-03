#!/usr/bin/env python3

import collections

Coordinate = collections.namedtuple('Coordinate', 'x y')
CoordinateWithSteps = collections.namedtuple('Coordinate', 'x y steps')

def get_all_horizontal_coords(start, end):
    lowest = min(start.x, end.x)
    highest = max(start.x, end.x)
    result = set()
    #print("HORIZONTAL lowest={}, highest={}".format(lowest, highest))
    for x in range(lowest, highest):
        result.add(Coordinate(x=x, y=start.y))
    return result

def get_all_vertical_coords(start, end):
    lowest = min(start.y, end.y)
    highest = max(start.y, end.y)
    result = set()
    #print("VERTICAL lowest={}, highest={}".format(lowest, highest))
    for y in range(lowest, highest):
        result.add(Coordinate(x=start.x, y=y))
    return result

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


def get_segment_coordinates(start, end):
    result = set()
    if start.x == end.x:
        result = get_all_vertical_coords(start, end)
    elif start.y == end.y:
        result = get_all_horizontal_coords(start, end)

    return result

def get_trace(wire, start):
    visited_coords = set()
    for segment in wire:
        end = get_end_coordinate(start, segment)
        visited_coords = visited_coords.union(get_segment_coordinates(start, end))
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

    both_visited = wire_1_visited.intersection(wire_2_visited)
    sorted_visited = sorted(both_visited, key = lambda coord: manhattan_distance(start, coord))
    print("A, answer: {}".format(manhattan_distance(start, sorted_visited[0])))

def b(input_data):
    start = Coordinate(x=0, y=0)
    wire_1 = input_data[0]
    wire_2 = input_data[1]




if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = [x.split(',') for x in f.readlines()]
    
    a(input_data)
    b(input_data)
    




