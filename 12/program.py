#!/usr/bin/env python3

import math
from collections import namedtuple

Coordinate = namedtuple('Coordinate', 'x y z')

VELOCITY_MAP = {}
COORDINATE_MAP = {}

def add_coordinates(a, b):
    x = a.x + b.x
    y = a.y + b.y
    z = a.z + b.z

    return Coordinate(x,y,z)


def apply_gravity(coords, vels):
    delta_v = []

    if vels in VELOCITY_MAP:
        return VELOCITY_MAP[vels]

    for c1 in coords:
        x_delta = 0
        y_delta = 0
        z_delta = 0
        for c2 in coords:

            if c1.x > c2.x:
                x_delta = x_delta - 1
            elif c1.x < c2.x:  
                x_delta = x_delta + 1

            if c1.y > c2.y:
                y_delta = y_delta - 1
            elif c1.y < c2.y:  
                y_delta = y_delta + 1

            if c1.z > c2.z:
                z_delta = z_delta - 1
            elif c1.z < c2.z:  
                z_delta = z_delta + 1

        delta_v.append(Coordinate(x_delta,y_delta,z_delta))

    new_vels = []
    for i in range(len(vels)):
        new_vels.append(add_coordinates(vels[i], delta_v[i]))

    VELOCITY_MAP[vels] = new_vels
    return new_vels

def apply_velocity(coords, vels):

    if coords in COORDINATE_MAP:
        return COORDINATE_MAP[coords]

    new_coords = []
    for i in range(len(coords)):
        new_coords.append(add_coordinates(coords[i], vels[i]))

    COORDINATE_MAP[coords] = coords
    return new_coords


def a(start_coords, start_vels):

    coords = start_coords
    vels = start_vels
    for x in range(1000):
        vels = apply_gravity(coords, vels)
        coords = apply_velocity(coords, vels)

    e_p = [abs(c.x) + abs(c.y) + abs(c.z) for c in coords]
    e_k = [abs(v.x) + abs(v.y) + abs(v.z) for v in vels]
    
    energy_count = 0
    for i in range(0,4):
        energy_count = energy_count + (e_p[i] * e_k[i])

    print("A, answer: {}".format(energy_count))
    
def b(start_coords, start_vels):
    coords = start_coords
    vels = start_vels
    
    while(True):
        vels = apply_gravity(coords, vels)
        coords = apply_velocity(coords, vels)

        if coords == start_coords and vels == start_vels:
            break
        


        
if __name__ == '__main__':

    m1 = Coordinate(x=-10, y=-13, z=7)
    m2 = Coordinate(x=1, y=2, z=1)
    m3 = Coordinate(x=-15, y=-3, z=13)
    m4 = Coordinate(x=3, y=7, z=-4)

    v1 = Coordinate(0, 0 ,0)
    v2 = Coordinate(0, 0 ,0)
    v3 = Coordinate(0, 0 ,0)
    v4 = Coordinate(0, 0 ,0)

    coordinates = [m1, m2, m3, m4]
    velocities = [v1, v2, v3, v4]

    #a(coordinates, velocities)
    #b(coordinates, velocities)

    print(Coordinate(1,2,3) == Coordinate(1,2,3))
    




