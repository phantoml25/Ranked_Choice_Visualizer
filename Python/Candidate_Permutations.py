# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 05:40:38 2020

@author: Kevin Adams

Changelog:
    1/16/21:
        Updated documentation
        Added definitions for Biased methods
Todo:
    Import PyApp for distribution
    change permutations to dictionary using abbreviations as keys
    
    create functions to import CSV with permutations
    create function to create polls with bias for second/third choice
"""

import matplotlib.pyplot as plt
import numpy as np
import time
from numpy.random import choice
from numpy.random import default_rng
import PySimpleGUI as sg

a = 0
l = []
final = []
cand_dict = dict({})
initials = dict({})

"""
******************************************************************************
Section Break: Entering Common Section
******************************************************************************
"""

def get_key(val,inits):
    for key, value in inits.items():
         if val == value:
             return key
 
    return "key doesn't exist"

"""
Precondition:
    Do not call directly, call candidates(a) with list
Returns in the form 
{
    abbr:total,...
}

"""
def heap(size,n=a,verbose=False):

    global l
    global final
    if size == 1:
        final.append([0,l.copy()])

        
    for x in range(size):
        heap(size-1,n,verbose)
        
        if(size%2) ==1:
            t = l[0]
            l[0]=l[size-1]
            l[size-1]=t
        else:
            t = l[x]
            l[x] = l[size-1]
            l[size-1] = t

    return 

"""
Precondition:
    s is a list of candidate names
    
Postcondition:
    s is unchanged
    a new list (final) of candidate combinations is returned
    final is formatted for use with the abbreviations function
    
    format for final:
        [ [0,[permutation]],...]
"""
def candidates(s):
    global l
    global a
    global final
    l = s
    a = len(l)
    heap(a)
    return final

"""
this function creates a dictionary of permutation acronyms
Precondition:
    cand is formatted as a list of strings
Postcondition:
    global dicitonaries created for tally and translation
    
    returns 2 dictionaries

"""
def dict_compile(cand):
    global cand_dict
    global final
    global initials
    
    #check for duplicate candidate initials
    for x in range(len(cand)):
        if cand[x][0] in initials:
            if initials[cand[x][0]] == cand[x]:
                break
            i = 1
            while i<len(cand[x]):
                if cand[x][i] not in initials:
                    break
                elif initials[cand[x][i]] == cand[x]:
                    break
                i+=1
            if i<=len(cand[x]):
                    initials[cand[x][i]] = cand[x]
        else:
            initials[cand[x][0]] = cand[x]
    
    candidates(cand)

    for i in range(len(final)):
        abb = ""
        for j in final[i][1]:
            abb = abb + get_key(j,initials)
        cand_dict[abb] = 0
    
    return cand_dict, initials

#element format: [count,'abbr',[list]]
def tally(candidates,permutations,initials):
    top = {}
    for x in range(len(candidates)):
        top[candidates[x]] = 0
    
    for x in list(permutations.keys()):
        first = initials[x[0]]
        top[first] = top[first] + permutations[x]
        
    return top

def tally_all(candidates,permutations,initials):
    results = {}
    for x in range(len(candidates)):
        results[candidates[x]] = 0
    
    for y in list(permutations.keys()):
        for i in range(len(y)):
            cand = initials[y[i]]
            results[cand][i] = results[cand][i] + permutations[y]
        
    return results

"""
******************************************************************************
Section Break: Entering Normal Generation
******************************************************************************
"""

"""
cand:
    list of candidate names
polls:
    array containing predicted first place numbers
    (polls from plurality voting system goes here)
    must be same length as cand
    assumes equal preference for candidates after first choice
population:
    integer with voting population
    
postcondition:
    return dictionary cand_dict
"""
def gen_permutations(cand,polls,population):
    global initials
    global cand_dict

    dict_compile(cand)
    
    weight = []
    combo = []
    
    for x in cand_dict:
        combo = []
        for y in range(len(cand)):
            chance = cand.index(initials[x[y]])
            combo.append(polls[chance]/((y+1)*2))
        #print(combo)
        weight.append(np.prod(combo))
        
    l = sum(weight)
    for x in range(len(weight)):
        weight[x] = weight[x]/l
        
    for x in range(population):
        h = np.random.choice(list(cand_dict.keys()),replace=True,p=weight)
        cand_dict[h] +=1
        if x%100 == 0:
            print("{:.4%} done".format(x/population))
    
    return cand_dict

"""
precondition:
    candidate_list = list in format [cand_A,cand_B,Cand_C,...]
    permutations = dictionary with permutations as keys
    population = integer == total of x's in permutations

postcondition:
    Creates a graph showing how many people voted for each combination of candidates,
    as well as a table of each candidate's 1st, second, and 3rd choice votes
"""
def graph_picks(candidate_list,permutations,population):
    global initials
    cand = candidate_list
    comb = permutations.copy()
    top = tally(cand,comb,initials)
    
    top3 = [cand]
    row = [0]*len(cand)
    
    
    return 0

"""
precondition:
    candidate_list = list in format [cand_A,cand_B,Cand_C,...]
    permutations = dictionary with permutations as keys
    population = integer == total of x's in permutations

postcondition:
    creates graph showing plurality winner and ranked choice winner comparison
"""
def calculate_results(candidate_list,permutations,population,visible=False):
    global initials
    cand = candidate_list
    comb = permutations.copy()
    top = tally(cand,comb,initials)
    
    top3 = [cand]
    row = [0]*len(cand)
    
    top3.append(list(top.values()))

    for x in range(2):
        top3.append(row.copy())
    
    losers = []
    print(initials)
    print(top)
    values = top.values()
    keys = top.keys()
        
    top_copy = top.copy()
    
    while max(top.values())/population < .5:
        loss = min(top.keys(), key=(lambda k: top[k]))
        l = get_key(loss,initials)
        print("Removing bottom candidate: ",loss,l)
        for x in list(comb.keys()):
            i = 0
            while (x[i] in losers):
                i=i+1
            #need to pop this entry
            if x[i] == l:
                j = i+1
                while (x[j] in losers):
                    j = j+1
                new_cand = initials[x[j]]
                moved = comb[x]
                top[new_cand] = top[new_cand] + moved
                top[loss] = top[loss]-moved
                top3[j+1][cand.index(new_cand)] = top3[j+1][cand.index(new_cand)] + moved
                #top3[i+1][cand.index(loss)] = top3[i+1][cand.index(loss)] - moved
                
                print(top)
    
        losers.append(l)
        top.pop(loss)
        print("%s in the lead with %1.2f%% of the vote"
              %(max(top.keys()),(max(top.values())/population)*100))
    
    #now show how many 1st,2nd, and 3rd place votes each member had
    print(top3)

    cm = max(top.keys(), key=(lambda k: top[k]))
    om = max(top_copy.keys(), key=(lambda k: top_copy[k]))

    compare = [["Ranked Choice","1 Choice"],[cm,om],[top[cm],top_copy[om]]]
    #totals = tally_all(cand, permutations, initials)
    print(compare)
    values = top_copy.values()
    keys = top_copy.keys()

    if cm is not om:
        print("ranked choice has produced a different result")
        return top3,1
    else:
        return top3,0

"""
Single function to automatically perform all tasks and output graph
"""
def Ranked_Choice_method(cand,population,polls):
    comb = gen_permutations(cand,polls,population)
    return graph_results(cand,comb,population)

"""
******************************************************************************
Section Break: Entering Biased Generation
******************************************************************************
"""

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
def Biased_Permutations(cand,population,first_choice,bias=[],window = 0):
    global cand_dict
    if len(first_choice) != len(cand):
        raise IndexError("first_choice incorrect length")
    if sum(first_choice) != 1:
        raise ValueError("first_choice doesn't total 1")
    
    if len(bias) == 0:
        bias = Bias_Generator(cand)
    
    comb,inits = dict_compile(cand)
    #comb = [0,abbr,[permutation],...]
    
    if window !=0:
        window['progress_description'].update(value="Generating Data")
    
    for x in range(population):
        f = np.random.choice(len(cand),replace=True,p=first_choice)
        abbr = get_key(cand[f],inits)
        biased = bias[f]
        #first choice established, generate rest of choices based on bias
        n = np.random.choice(len(cand)-1,size=len(cand)-1,replace=False,p=biased)
        for y in n:
            if y>=f:
                abbr += get_key(cand[y+1], inits)
            else:
                abbr += get_key(cand[y], inits)
            
        comb[abbr] +=1
        if x%(population/1000) < 0.5:
            if window != 0:
                window['progress'].update(current_count= x, max=population)
                window['completion'].update(value=int((x/population)*100))
                window.refresh()
            else:
                print("{:.4%} done".format(x/population))
    
    return comb

"""
Single function to automatically perform all tasks and output graph
"""
def Biased_Ranked_Choice_method(cand,population,polls,bias=[],window=0):
    comb = Biased_Permutations(cand,population,polls,bias=bias,window=window)
    return calculate_results(cand,comb,population)