# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 03:10:32 2020

@author: Kevin
"""

from Candidate_Permutations import *

population = 328000
cand = ['control','meh','socialist']

comb = gen_permutations(cand,[.3,.2,.5],population)

print(comb)

#graph_results(cand,comb,population)

