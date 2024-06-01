# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 19:00:07 2024

@author: gava1
"""

x= 500 

def foo(y):
    return x+y
x=2000 
z= foo(307)

print(f'x z and foo: {x}, {z}, {foo}')

def bar(x):
    x = 1000
    return foo(308)

w= bar(349)

print(f"x and w: {x}, {w}")

def double(x):
    return 2*x
myfunc= double

print(myfunc(21))

def make_adder(n):
    return lambda x: x+n

functions= []
for i in range(5):
    functions.append(make_adder(i))

for f in functions:
    print(f(12))
