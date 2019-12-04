#!/usr/bin/env python3

def check_non_decreasing(number):
    highest = '0'
    for x in str(number):
        if x < highest:
            return False
        highest = x
    return True

def contains_triple_digit(number, digit):
    if '{}{}{}'.format(digit, digit, digit) in str(number):
        return True
    return False

def check_double_digit(number):
    for x in '1234567890':
        if '{}{}'.format(x,x) in str(number):
            return True
    return False

def check_strict_double_digit(number):
    for x in '1234567890':
        if '{}{}'.format(x,x) in str(number):
            if not contains_triple_digit(number, x):
                return True
    return False
    
def a(lower_limit, higher_limit):
    candidate_solutions = []
    for candidate in range(int(lower_limit), int(higher_limit)):
        ok = check_non_decreasing(candidate)
        if ok:
            ok = check_double_digit(candidate)
        if ok: 
            candidate_solutions.append(candidate)
    
    print("A, answer: {}".format(len(candidate_solutions)))

def b(lower_limit, higher_limit):
    candidate_solutions = []
    for candidate in range(int(lower_limit), int(higher_limit)):
        ok = check_non_decreasing(candidate)
        if ok:
            ok = check_strict_double_digit(candidate)
        if ok: 
            candidate_solutions.append(candidate)
    
    print("B, answer: {}".format(len(candidate_solutions)))
        
if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = f.readline().split('-')
    lower_limit = input_data[0]
    higher_limit = input_data[1]

    a(lower_limit, higher_limit)
    b(lower_limit, higher_limit)
    