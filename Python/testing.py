# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 03:10:32 2020

@author: Kevin
"""

from Candidate_Permutations import *

population = 32800
cand = ['Abe','Beckket','Calliway','Abby']
comb = [['B','C'],
        ['A','C'],
        ['A','B']]
test = []
#comb = gen_permutations(cand,[.3,.2,.5],population)
"""
for i in range(3):
    run = Bias_Generator(cand)
    test.append(run)
    fig1, ((ax1,ax3),(ax2,ax4)) = plt.subplots(nrows=2,ncols=2)
    ax1.pie([float(v) for v in run[0]], labels=[str(k) for k in comb[0]],autopct='%1.2f%%')
    ax2.pie([float(v) for v in run[1]], labels=[str(k) for k in comb[1]],autopct='%1.2f%%')
    ax3.pie([float(v) for v in run[2]], labels=[str(k) for k in comb[2]],autopct='%1.2f%%')
    

print(test)
    
#print(comb)

#graph_results(cand,comb,population)
"""

first_Choice = [.31,.1,.29,.30]
print(Biased_Ranked_Choice_method(cand,population,first_Choice))