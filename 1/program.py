#!/usr/bin/env python3

import math

def calculate_fuel(mass):
    fuel = math.floor(mass/3.0) - 2
    return max(fuel,0)

def calculate_total_fuel(mass):
    fuel = calculate_fuel(mass)
    total_fuel = fuel

    while(fuel > 0):
        fuel = calculate_fuel(fuel)
        total_fuel += fuel
    
    return total_fuel


def a(input_data):
    fuel_usages = [calculate_fuel(x) for x in input_data]
    total_fuel = sum(fuel_usages)
    print("A, answer: {}".format(total_fuel))

def b(input_data):
    fuel_usages = [calculate_total_fuel(x) for x in input_data]
    total_fuel = sum(fuel_usages)
    print("B, answer: {}".format(total_fuel))


if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = [int(x.strip()) for x in f.readlines()]
    
    a(input_data)
    b(input_data)
    




