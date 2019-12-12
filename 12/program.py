#!/usr/bin/env python3

import math
from collections import namedtuple

Coordinate = namedtuple('Coordinate', 'x y z')

def add_coordinates(a, b):
    x = a.x + b.x
    y = a.y + b.y
    z = a.z + b.z

    return Coordinate(x,y,z)


def apply_gravity(coords, vels):
    delta_v = []
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

    return new_vels

def apply_velocity(coords, vels):
    new_coords = []
    for i in range(len(coords)):
        new_coords.append(add_coordinates(coords[i], vels[i]))

    return new_coords


def a(start_coords, start_vels):

    coords = start_coords
    vels = start_vels
    for x in range(1000):
        vels = apply_gravity(coords, vels)
        print("New velocities: {}\n {}\n {}\n {}".format(vels[0], vels[1], vels[2], vels[3]))
        coords = apply_velocity(coords, vels)
        print("New coordinates: {}\n {}\n {}\n {}".format(coords[0], coords[1], coords[2], coords[3]))

    e_p = [abs(c.x) + abs(c.y) + abs(c.z) for c in coords]
    e_k = [abs(v.x) + abs(v.y) + abs(v.z) for v in vels]
    
    energy_count = 0
    for i in range(0,4):
        energy_count = energy_count + (e_p[i] * e_k[i])

    print("A, answer: {}".format(energy_count))
    
def b(input_data):
    pass

        
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

    a(coordinates, velocities)
    #b(input_data.copy())
    




