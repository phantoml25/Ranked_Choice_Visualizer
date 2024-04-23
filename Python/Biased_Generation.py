# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 14:32:41 2021

@author: Kevin

Holds functions for Biased Generation
"""

import matplotlib.pyplot as plt
import numpy as np
import time
from numpy.random import choice
from numpy.random import default_rng

from Candidate_Permutations import dict_compile
from Candidate_Permutations import graph_results
from Candidate_Permutations import get_key

"""
Generate random biases for a candidate list
"""
def Bias_Generator(cand):
    bias = []
    
    for i in range(len(cand)):
        b = []
        temp = np.random.rand(len(cand)-1)
        total = sum(temp)
        for j in range(len(temp)):
            b.append(temp[j])
            b[j] = b[j]/total
        bias.append(b)
        
    return bias
    

"""
Biased_Permutations
generate list of possible ranked choice results based on:
    single-choice polls
    presumed biases for candidates among voters
        ex: party affiliation, etc.
Precondition:
    cand = list with format [cand_A,cand_B,cand_C]
    perm = list with format [[0,abbr,]]
    population = integer total population size
    first_choice = poll ratio of first choice votes
        format = [.a,.b,.c,...] total == 1 && len == len(cand)
    (optional) bias = list with format [[cand,[bias_next]]]
        where bias_next is list of ratios for next candidate preference
        ex: cand = [a,b,c]
            bias = [[a,[.6,.4]],
                    [b,[.7,.3]],
                    [c,[.5,.5]]]
        If bias is not given, random biases will be generated
    
"""
def Biased_Permutations(cand,population,first_choice,bias=[]):
    global cand_dict
    if len(first_choice) != len(cand):
        raise IndexError("first_choice incorrect length")
    if sum(first_choice) != 1:
        raise ValueError("first_choice doesn't total 1")
    
    if len(bias) == 0:
        bias = Bias_Generator(cand)
    
    comb,inits = dict_compile(cand)
    #comb = [0,abbr,[permutation],...]
    
    for x in range(population):
        f = np.random.choice(len(cand),replace=True,p=first_choice)
        
        comb[f] +=1
        if x%10000 == 0:
            print("{:.4%} done".format(x/population))
    
    return comb

"""
Single function to automatically perform all tasks and output graph
"""
def Biased_Ranked_Choice_method(cand,population,polls,bias=[]):
    comb = Biased_Permutations(cand,population,polls,bias)
    return graph_results(cand,comb,population)