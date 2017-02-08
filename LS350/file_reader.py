# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:32:54 2017

@author: Cryogenic System
"""

import pickle

with open('test.dat', 'r+b') as f:
    print("Here")
    print(pickle.load(f))
    for line in f:
        print("line")
        print(pickle.load(line))