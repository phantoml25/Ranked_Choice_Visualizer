# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 05:40:38 2020

@author: Kevin Adams

Changelog:
    1/16/21:
        Updated documentation
    
Todo:
    create functions to import CSV with permutations
    create function to create polls with bias for second/third choice
"""

import matplotlib.pyplot as plt
import numpy as np
import time
from numpy.random import choice

a = 0
l = []
final = []


"""
Precondition:
    Do not call directly, call candidates(a) with list
Returns in the form 
[
   [count,index,[permutation]]
]
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
this function creates abbreviations for each permutation
possibly unneeded
Precondition:
    fin is a list formatted as:
        [ [0,[permutation]],...]    
Postcondition:
    list "new" created with format
        [ [0,abbr,[permutation]],...]
    return list "new"

possible changes:
    need to handle duplicate first letters    
"""
def abbreviations(fin):
    new = []
    flen = len(fin)
    for i in range(flen):
        row = fin[i][1]
        ab = ''
        for j in range(len(row)):
            ab += row[j][0]
        new.append([fin[i][0],ab,fin[i][1]])
    return new
    
#element format: [count,'abbr',[list]]
def tally(candidates,permutations):
    top = {}
    for x in range(len(candidates)):
        top[candidates[x]] = 0
    
    for x in range(len(permutations)):
        first = permutations[x][2][0]
        top[first] = top[first] + permutations[x][0]
        
    return top

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
    return list with format
        [[x,abbr,[permuation]],...]
        x = tally for this permuatation
        abbr = abbreviation for the permutation
"""
def gen_permutations(cand,polls,population):
    
    comb = candidates(cand)

    comb = abbreviations(comb)
    
    weight = []
    combo = []
    
    for x in range(len(comb)):
        combo = []
        for y in range(len(cand)):
            chance = cand.index(comb[x][2][y])
            combo.append(polls[chance]/((y+1)*2))
        #print(combo)
        weight.append(np.prod(combo))
        
    l = sum(weight)
    for x in range(len(weight)):
        weight[x] = weight[x]/l
        
    for x in range(population):
        h = np.random.choice(range(len(comb)),replace=True,p=weight)
        comb[h][0] +=1
        if x%10000 == 0:
            print("{:.4%} done".format(x/population))
    
    return comb

"""
precondition:
    candidate_list = list in format [cand_A,cand_B,Cand_C,...]
    permutations = list in format [[x,abbr,[permutation]],...]
    population = integer == total of x's in permutations

postcondition:
    creates graph showing plurality winner and ranked choice winner comparison
"""
def graph_results(candidate_list,permutations,population):
    cand = candidate_list
    comb = permutations.copy()
    top = tally(cand,comb)
    
    print(top)
    values = top.values()
    keys = top.keys()
    
    print(values)
    csum = 0
    
    top_copy = top.copy()
    
    rem = 1
    
    while max(top.values())/population < .5:
        loss = min(top.keys(), key=(lambda k: top[k]))
        l = loss[0]
        #print("Removing bottom candidate: ",loss)
        for x in range(len(comb)):
            h = 0
            new = comb[x][2][h]
            while new not in top.keys():
                h += 1
                if h >= len(comb[x][2]):
                    break
                else:
                    new = comb[x][2][h]
            if loss == comb[x][2][h]:
                new = comb[x][2][h+1]
                top[new] = top[new] + comb[x][0]
        top.pop(loss)
        #print(top,"Total: ",population)
        #print("Top contender: {:.2%}".format(max(top.values())/population))
    
    #now show how many 1st,2nd, and 3rd place votes each member had
    top3 = [cand]
    row = [0]*len(cand)

    for x in range(3):
        top3.append(row.copy())

    print(top3)

    for x in range(len(comb)):
        row = comb[x]
        a = cand.index(row[2][0])
        b = cand.index(row[2][1])
        c = cand.index(row[2][2])
        top3[1][a] = top3[1][a] + row[0]
        top3[2][b] = top3[2][b] + row[0]
        top3[3][c] = top3[3][c] + row[0]

    print(top3)

    cm = max(top.keys(), key=(lambda k: top[k]))
    om = max(top_copy.keys(), key=(lambda k: top_copy[k]))

    fig1, ((ax1,ax3),(ax2,ax4)) = plt.subplots(nrows=2,ncols=2)
    ax1.pie([float(v) for v in values], labels=[str(k) for k in keys],autopct='%1.2f%%')
    ax1.set_title("Ranked choice votes")
    ax1.axis('equal')

    Cols=["Votes","1st","2nd","3rd"]

    compare = [["Ranked Choice","1 Choice"],[cm,om],[top[cm],top_copy[om]]]

    print(compare)
    ax2.table(cellText=top3,rowLabels=Cols,loc='center')
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    ax2.set_title("Ranked Choice Winner: %s"%(cm))

    ax4.table(cellText=compare,loc='center')
    ax4.get_xaxis().set_visible(False)
    ax4.get_yaxis().set_visible(False)
    plt.box(on=None)
    ax4.set_title("1st choice Winner: %s"%(om))
    values = top_copy.values()
    keys = top_copy.keys()

    ax3.pie([float(v) for v in values], labels=[str(k) for k in keys],autopct='%1.2f%%')
    ax3.set_title("1st choice votes")
    ax3.axis('equal')



    plt.show()
    if cm is not om:
        print("ranked choice has produced a different result")
        return 1
    else:
        return 0
        
    
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
    bias = list with format [[cand,[bias_next]]]
        where bias_next is list of ratios for next candidate preference
        ex: cand = [a,b,c]
            bias = [[a,[.6,.4]],
                    [b,[.7,.3]],
                    [c,[.5,.5]]]
    
    
"""
def Biased_Permutations(cand,permutations,population,first_choice,bias):
    if len(first_choice) != len(cand):
        raise IndexError("first_choice incorrect length")
    if sum(first_choice) != 1:
        raise ValueError("first_choice doesn't total 1")
    
    comb = candidates(cand)
    comb = abbreviations(comb)
    #comb = [0,abbr,[permutation],...]
    
    for x in range(population):
        
    
    return comb


"""
Single function to automatically perform all tasks and output graph
"""
def Ranked_Choice_method(cand,population,polls):
    comb = gen_permutations(cand,polls,population)
    return graph_results(cand,comb,population)
