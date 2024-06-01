# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:09:14 2024

@author: gava1
"""

def gen1():
    yield 1
    yield 2
    
def gen3():
    yield from gen1()

for i in gen3():
    print(i)
    
def negate_elements(x):
    out = []
    for val in x:
        out.append(-val)
    return out

def traverse_tree(tree):
    if isinstance(tree, list):  # If the current node is a list
        for node in tree:  # Iterate over each element in the list
            yield from traverse_tree(node)  # Recursively traverse the subtree
    else:  # If the current node is not a list (i.e., it's a leaf node)
        if isinstance(tree, int):  # Check if the node is an integer
            yield tree 
        
        
tree = [13, [7], [8, [99], [16, [77]], [42]]]
for node_value in traverse_tree(tree):
    print(node_value)
