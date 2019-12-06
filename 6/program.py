#!/usr/bin/env python3
            
class Node:
    def __init__(self, name, parent_node):
        self.name = name
        self.children = []
        self.parent = parent_node
        if parent_node is not None:
            parent_node.add_child(self)
    
    def add_child(self, child):
        self.children.append(child)

    def count_depth_traversive(self, depth, count):
        new_count = count + depth
        for child in self.children:
            new_count = new_count + child.count_depth_traversive(depth + 1, count)

        return new_count

    def get_parents(self, parents):
        if self.parent is None:
            return parents
        else:
            return self.parent.get_parents(parents + [self.parent.name])
        
def initialize_tree(structured_data, root_node_name):
    root_node = Node(root_node_name, None)
    
    for child in structured_data[root_node_name]:
        add_node(structured_data, child, root_node)

    return root_node

def add_node(structured_data, name, parent_node):
    node = Node(name, parent_node)
    if name in structured_data:
        for child in structured_data[name]:
            add_node(structured_data, child, node)


def populate_dict(input_data):
    data = {}
    all_parents = set()
    all_children = set()

    for x in input_data:
        [parent, child] = x
        all_parents.add(parent)
        all_children.add(child)
        
        if parent in data:
            data[parent].append(child)
        else:
            data[parent] = [child]
    
    center_of_mass = all_parents.difference(all_children)

    if len(center_of_mass) != 1 :
        # I did not understand that the start-node was always named COM...
        raise RuntimeError("Center of mass is not well defined with len={}".format(len(center_of_mass)))

    return data, center_of_mass.pop()

def find_node_by_name(node, name):
    if node.name == name:
        return node
    else:
        foundNode = None
        for child in node.children:
            foundNode = find_node_by_name(child, name)
            if foundNode != None:
                return foundNode
        return foundNode

def calculate_number_of_jumps(parents_a, parents_b):
    for x in parents_a:
        if x in parents_b:
            return parents_a.index(x) + parents_b.index(x)


def a_and_b(input_data):
    structured_data, center_of_mass = populate_dict(input_data)
    root_node = initialize_tree(structured_data, center_of_mass)
    print("A, answer: {}".format(root_node.count_depth_traversive(0,0)))

    you = find_node_by_name(root_node, 'YOU')
    you_parents = you.get_parents([])

    san = find_node_by_name(root_node, 'SAN')
    san_parents = san.get_parents([])

    nr_jumps = calculate_number_of_jumps(you_parents, san_parents)
    print("B, answer: {}".format(nr_jumps))


if __name__ == '__main__':
    f = open("input.txt", "r")
    input_data = [x.strip().split(')') for x in f.readlines()]
    
    a_and_b(input_data.copy())
    
    




