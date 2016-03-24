# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 13:06:52 2015

@author: mounik
"""
import sys
import re
import itertools


        
def GenerateAllHashTables(omniList, tableOrderNumber, bucketSize):
    hashTableList = []
    for elementList in omniList:
        dictHashTable = {}
        for singleList in elementList:
            sumItems = 0
            for item in singleList:
                sumItems += ord(item)
            modValue = sumItems%bucketSize
            dictHashTable[modValue]= dictHashTable.get(modValue,0)+1
        hashTableList.append(dictHashTable)
    print(hashTableList[tableOrderNumber])
        
def GenerateOmniList(inputData,tableOrderNumber):
    omniList = [[] for i in range(tableOrderNumber+1)]
    combinationList = []

    for line in inputData:
        line = re.findall('\w',line)
        lines = sorted(line)
        
        for ind in xrange(1,len(lines)+1):
            combo = [list(x) for x in itertools.combinations(lines, ind)]
            combinationList.extend(combo)    
    for ind1 in range (len(omniList)):
        for item in combinationList:
            if(ind1 == len(item)):
                omniList[ind1].append(item)
    return omniList   
    

def GenerateFutureFrequentItems(lstFrequentItemSets, maxPossibleElements, lstInputData, inputData, support, bucketSize):
    lstFreqItems = []
    lstFreqItems = lstFrequentItemSets
    omniList = []
    omniList = GenerateOmniList(inputData,maxPossibleElements)
    dictCountItemSets = {}
    while(len(lstFreqItems)>0):
        for i in range(maxPossibleElements):
            for pairInd1 in range(len(lstFreqItems)):
                for pairInd2 in range(pairInd1+1, len(lstFreqItems)):
                    setA = set(lstFreqItems[pairInd1]+lstFreqItems[pairInd2])
                    sortedList = sorted(list(setA))
                    if(len(sortedList) == len(lstFreqItems[pairInd1])+1):
                        count =0
                        for sinTrans in lstInputData:
                            if(set(sortedList).issubset(set(sinTrans))):
                                count += 1                        
                        dictCountItemSets[tuple(sortedList)] = count
        
        lstFreqItems = []
        for item in dictCountItemSets:
            if(dictCountItemSets[item]>=support):
                lstFreqItems.append(list(item))
        dictCountItemSets.clear()
        lstElementCount = []
        if(len(lstFreqItems) > 0):
            for index in range(len(lstFreqItems)):
                lstElementCount.append(len(lstFreqItems[index]))
            GenerateAllHashTables(omniList,max(lstElementCount),bucketSize)
            print(sorted(lstFreqItems))
            
        

def ExecuteSecondPass(inputData,lstSingleFrequentItems, dictPairs, support, bucketSize):
    
    # Form pairs from the frequent itemsets generated from the first pass
    
    dictPossibleCandidatePairs = {}
    lstFrequentPairs = []
    lstLengthOfEachTrasaction= []
    lstInputData= []
    
    for line in inputData:
        line = re.findall('\w',line)
        lines = sorted(line)
        lstLengthOfEachTrasaction.append(len(lines))
        lstInputData.append(lines)
        
        for ind1 in range(len(lines)):
            for ind2 in range(ind1+1, len(lines)):
                lstDoublePair = []
                lstDoublePair.append(lines[ind1])
                lstDoublePair.append(lines[ind2])
                count= 0
                for item in lstDoublePair:
                    if item in lstSingleFrequentItems:
                        count += 1
                if(count== 2):
                    mod1Value = (ord(lines[ind1])+ord(lines[ind2]))%bucketSize
                    if(dictPairs[mod1Value] !=0):
                        dictPossibleCandidatePairs[tuple(lstDoublePair)] =dictPossibleCandidatePairs.get(tuple(lstDoublePair),0)+1
    
    
    for item in dictPossibleCandidatePairs:
        if(dictPossibleCandidatePairs[item] >= support):
            lstFrequentPairs.append(list(item))
    print(sorted(lstFrequentPairs))
    inputData.close()
    inputData=open(sys.argv[1])
    GenerateFutureFrequentItems(lstFrequentPairs, max(lstLengthOfEachTrasaction), lstInputData, inputData, support, bucketSize)    
 

def ExecuteFirstPass(inputData, support, bucketSize):
    lstSingleCandidates= []
    dictItemCount = {}
    hashTableDict = {}
    for line in inputData:
        line = re.findall('\w+', line)
        lines= sorted(line)
        for item in lines:
            dictItemCount[item] = dictItemCount.get(item,0)+1

        for index in range(len(lines)):
            for ind in range(index+1, len(lines)):
                modValue = (ord(lines[index])+ord(lines[ind]))%bucketSize
                hashTableDict[modValue] = hashTableDict.get(modValue,0)+1

    for element in dictItemCount:
        if(dictItemCount[element] >= support):
            lstSingleCandidates.append(element)
    
    print(sorted(lstSingleCandidates))
    print(hashTableDict)
    #Replacing the values of the dictionary by bit maps
    for element in hashTableDict:
        if(hashTableDict[element]>= support):
            hashTableDict[element]=1
        else:
            hashTableDict[element]=0
    return sorted(lstSingleCandidates), hashTableDict


if __name__ == '__main__':
    inputData=open(sys.argv[1])
    support = int(sys.argv[2])
    bucketSize = int(sys.argv[3])
    frequentItemList = []
    hashTableDict = {}
    frequentItemList, hashTableDict=ExecuteFirstPass(inputData, support, bucketSize)
    inputData.close()
    inputData= open(sys.argv[1])
    ExecuteSecondPass(inputData,frequentItemList, hashTableDict, support, bucketSize)

