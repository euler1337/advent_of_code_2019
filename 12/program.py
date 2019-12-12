#!/usr/bin/env python3

import math
from collections import namedtuple

class CoordinateContainer:
    def __init__(self, coords):
        self.content = coords

Coordinate = namedtuple('Coordinate', 'x y z')

DELTA_V_MAP = {}
COORDINATE_MAP = {}

def add_coordinates(a, b):
    x = a.x + b.x
    y = a.y + b.y
    z = a.z + b.z

    return Coordinate(x,y,z)

def calcualte_delta_v(coords):
    sorted_coords = sorted(coords)
    c_0 = sorted_coords[0]
    c_1 = sorted_coords[1]
    c_2 = sorted_coords[2]
    c_3 = sorted_coords[3]

    hashed = str(coords)
    if hashed in DELTA_V_MAP:
        delta_v =  DELTA_V_MAP[hashed] 
    else:
        delta_v =[]
        old_0 = coords[0]
        v0 = 3 * (old_0 == c_0) + (old_0 == c_1) - (old_0 == c_2) - 3 * (old_0 == c_3)

        old_1 = coords[1]
        v1 = 3 * (old_1 == c_0) + (old_1 == c_1) - (old_1 == c_2) - 3 * (old_1 == c_3)

        old_2 = coords[2]
        v2 = 3 * (old_2 == c_0) + (old_2 == c_1) - (old_2 == c_2) - 3 * (old_2 == c_3)

        old_3 = coords[3]
        v3 = 3 * (old_3 == c_0) + (old_3 == c_1) - (old_3 == c_2) - 3 * (old_3 == c_3) 

        delta_v = [v0,v1,v2,v3]
        hashed = str(coords)
        DELTA_V_MAP[hashed] = delta_v

    return delta_v

def apply_gravity(coords, vels):
    delta_v = calcualte_delta_v(coords)
    print("DELTA_V: {}".format(delta_v))
    return [sum(x) for x in zip(vels, delta_v)]

def apply_velocity(coords, vels):
    return [sum(x) for x in zip(coords, vels)]

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
    
def b():

    x_coords = [-1,2,4,3]
    y_coords = [0,-10,-8,5]
    z_coords = [2,-7,8,1]

    v_start = [0,0,0,0] 
    

    coords = y_coords
    vels = v_start
    i = 0
    for a in range(10):
        i = i + 1
        print("coords: {}".format(coords))
        vels = apply_gravity(coords, vels)
        coords = apply_velocity(coords, vels)

        if coords == y_coords and vels == v_start:
            print("Y repeats after: {} iterations".format(i))
            break


    coords = x_coords
    vels = v_start

    #i = 0
    #while(True):
    #    i = i + 1
    #    vels = apply_gravity(coords, vels)
    #    coords = apply_velocity(coords, vels)
#
#        if coords == x_coords and vels == v_start:
#            print("X repeats after: {} iterations".format(i))
#            break



        


        
if __name__ == '__main__':


    test1 = Coordinate(x=-1, y=0, z=2)
    test2 = Coordinate(x=2, y=-10, z=-7)
    test3 = Coordinate(x=4, y=-8, z=8)
    test4 = Coordinate(x=3, y=5, z=-1)

    m1 = Coordinate(x=-10, y=-13, z=7)
    m2 = Coordinate(x=1, y=2, z=1)
    m3 = Coordinate(x=-15, y=-3, z=13)
    m4 = Coordinate(x=3, y=7, z=-4)

    v1 = Coordinate(0, 0 ,0)
    v2 = Coordinate(0, 0 ,0)
    v3 = Coordinate(0, 0 ,0)
    v4 = Coordinate(0, 0 ,0)

    coordinates = [m1, m2, m3, m4]
    #coordinates = [test1, test2, test3, test4]
    velocities = [v1, v2, v3, v4]

    #a(coordinates, velocities)
    b()
    
    




