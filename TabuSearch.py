# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:30:20 2022

@author: eghorbanioskalaei
Tabu Search
"""
import random, math 

berlin52= [[565.0 ,575.0],[25.0, 185.0],[345.0 ,750.0],[945.0, 685.0],[845.0, 655.0],
           [880.0 ,660.0],[25.0, 230.0],[525.0 ,1000.0],[580.0, 1175.0],[650.0, 1130.0],
           [1605.0, 620.0],[1220.0, 580.0],[1465.0 ,200.0],[1530.0, 5.0],[845.0, 680.0],
           [725.0 ,370.0],[145.0 ,665.0],[415.0 ,635.0],[510.0, 875.0],[560.0, 365.0],
           [300.0 ,465.0],[520.0, 585.0],[480.0 ,415.0],[835.0, 625.0],[975.0, 580.0],
           [1215.0 ,245.0],[1320.0 ,315.0],[1250.0 ,400.0],[660.0, 180.0],[410.0 ,250.0],
           [420.0 ,555.0],[575.0, 665.0],[1150.0, 1160.0],[700.0, 580.0],[685.0, 595.0],
           [685.0 ,610.0],[770.0 ,610.0],[795.0 ,645.0],[720.0 ,635.0],[760.0, 650.0],
           [475.0, 960.0],[95.0, 260.0],[875.0, 920.0],[700.0, 500.0],[555.0, 815.0],
           [830.0, 485.0],[1170.0 ,65.0],[830.0, 610.0],[605.0 ,625.0],[595.0, 360.0],
           [1340.0, 725.0],[1740.0, 245.0]]

'''The initial solution is composed of random permutation of nodes'''
def constructInitialSolution(initPerm):
    #randomize the initial permutation
    permutation = initPerm[:] #make a copy of initial permutation
    size= len(permutation)
    for index in range(size):
        #shuffle the values of the initial permutation randomly
        #get a random index and exchange values
        shuffleIndex= random.randrange(index, size) #random range exclude upperbound
        permutation[shuffleIndex], permutation[index] = \
            permutation[index], permutation[shuffleIndex]
    return permutation
        
def tourCost(perm):
    totalDistance = 0.0
    size = len(perm)
    for index in range(size):
        startNode = perm[index]
        
        if index== size-1:
            endNode = perm[0]
        else:
            endNode = perm[index+1]
            
        totalDistance +=euclideanDistance(startNode, endNode)
    return totalDistance

def euclideanDistance(xNode, yNode):
    sum = 0.0
    for xi, yi in zip (xNode, yNode):
        sum+=pow((xi-yi),2)
    return math.sqrt(sum)

def stochasticTwoOptWithEdges(perm):
    result= perm[:]
    size= len(result)
    
    p1, p2 = random.randrange(0,size), random.randrange(0,size)
    exclude = set([p1])
    if p1==0:
        exclude.add(size-1)
    else:
        exclude.add(p1-1)
        
        
    if p1==size-1:
        exclude.add(0)
    else:
        exclude.add(p1+1)
    
    while p2 in exclude:
        p2= random.randrange(0, size)
        
    if p2 < p1:
        p1, p2 = p2 , p1
    
    result[p1:p2] = reversed(result[p1:p2])
    return result , [[perm[p1-1], perm[p1]], [perm[p2-1], perm[p2]]]

def locateBestNewSol(newSols):
    newSols.sort(key = lambda c:c["cost"])
    bestNewSol = newSols[0]
    return bestNewSol

def isTabu(aPermutation, tabuList):
    size= len(aPermutation)
    for index, node in enumerate(aPermutation):
        if index==size-1:
            nextNode= aPermutation[0]
        else:
            nextNode= aPermutation[index+1]
        edge= [node,nextNode]
        if edge in tabuList:
            return True
    return False

    

def generateNewSol(baseSol, bestSol, tabuList):
    newPermutation, edges, newSol = None, None, {}
    while newPermutation == None or isTabu(newPermutation, tabuList):
        newPermutation, edges = stochasticTwoOptWithEdges(baseSol["permutation"])
        if tourCost(newPermutation)< bestSol["cost"]:
            break
    
    newSol["permutation"] = newPermutation
    newSol["cost"] = tourCost(newSol["permutation"])
    newSol["edges"] = edges
    return newSol





algorithmName="Tabu Search"
print("best solution by "+ algorithmName+ "...")

#problem configuration
inputsTSP= berlin52
maxNewSols= 40
maxIterations = 5000
maxEdgesInTabuList = 1
k=5
credit= 0
tabuList = []

'''Construct the initial solution'''

bestSol={}
bestSol["permutation"]= constructInitialSolution(inputsTSP)
bestSol["cost"]= tourCost(bestSol["permutation"])
bestSol["edges"]= None
baseSol=bestSol



while maxIterations > 0:
    '''generate random neighbors solution'''
    newSols=[]
    for index in range(0, maxNewSols):
        newSol = generateNewSol(baseSol, bestSol, tabuList)
        newSols.append(newSol)
    '''select the best new solution'''
    bestNewSol = locateBestNewSol(newSols)
    
    delta = bestNewSol["cost"] - baseSol["cost"]
    if delta <=0:
        credit = -1+delta
        baseSol = bestSol # I don't understand why?
        '''selection of the best found solution so far'''
        if bestNewSol["cost"] <bestSol["cost"]:
            bestSol = bestNewSol
            print('it:', maxIterations, 'cost: %.2f' %bestSol["cost"])
            
            '''Updating the tabu list. The new movements are added and the oldest ones are removed, in case the list is full'''
            
                    
            for edge in bestNewSol["edges"]:
                tabuList.append(edge)
                if len(tabuList)> maxEdgesInTabuList:
                    del tabuList[0]
    else:
        if delta <= k* credit: #I don't understand why?
            credit = 0
            baseSol= bestNewSol
    maxIterations -=1
   
