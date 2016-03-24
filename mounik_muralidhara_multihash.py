# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 10:01:00 2015

@author: mounik
"""

import sys
import re
import itertools

def GenerateAllHashTables(omniList, tableOrderNumber, support, bucketSize):
    hashTableList1 = []
    hashTableList2 = []
    for elementList in omniList:
        dictHashTable1 = {}
        dictHashTable2 = {}
        for singleList in elementList:
            sumItems = 0
            for item in singleList:
                sumItems += ord(item)
            modValue1 = (9*sumItems)%bucketSize
            modValue2 = (7*sumItems)%bucketSize
            dictHashTable1[modValue1]= dictHashTable1.get(modValue1,0)+1
            dictHashTable2[modValue2]= dictHashTable2.get(modValue2,0)+1
        hashTableList1.append(dictHashTable1)
        hashTableList2.append(dictHashTable2)
    print(hashTableList1[tableOrderNumber])
    print(hashTableList2[tableOrderNumber])

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
            GenerateAllHashTables(omniList,max(lstElementCount), support, bucketSize)
            print(sorted(lstFreqItems))

def ExecuteSecondPass(inputData,lstSingleFrequentItems, dictPairs1, dictPairs2, support, bucketSize):
    
    # Form pairs from the frequent itemsets generated from the first pass
    
    dictPossibleCandidatePairs ={}
    lstFrequentPairs = []
    lstLengthOfEachTrasaction= []
    lstInputData= []
    
    for line in inputData:
        line = re.findall('\w',line)
        lines = sorted(line)
        lstLengthOfEachTrasaction.append(len(lines))
        lstInputData.append(lines)
        #Generating Pairs
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
                    mod1Value = (9*(ord(lines[ind1])+ord(lines[ind2])))%bucketSize
                    mod2Value = (7*(ord(lines[ind1])+ord(lines[ind2])))%bucketSize
                    if(dictPairs1[mod1Value] ==1 & dictPairs2[mod2Value] ==1):
                        dictPossibleCandidatePairs[tuple(lstDoublePair)] =dictPossibleCandidatePairs.get(tuple(lstDoublePair),0)+1
    
    
    for item in dictPossibleCandidatePairs:
        if(dictPossibleCandidatePairs[item] >= support):
            lstFrequentPairs.append(list(item))
    print(sorted(lstFrequentPairs))
    inputData.close()
    inputData=open(sys.argv[1])
    GenerateFutureFrequentItems(lstFrequentPairs, max(lstLengthOfEachTrasaction), lstInputData, inputData,support, bucketSize)

def ExecuteFirstPass(inputData, support, sizeOfBuckets):
    lstSingleCandidates= []
    dictItemCount = {}
    hashTableDict1 = {}
    hashTableDict2 = {}
    for line in inputData:
        line = re.findall('\w+', line)
        lines= sorted(line)
        for item in lines:
            dictItemCount[item] = dictItemCount.get(item,0)+1
                    

        for index in range(len(lines)):
            for ind in range(index+1, len(lines)):
                modValue1 = (9*(ord(lines[index])+ord(lines[ind])))%sizeOfBuckets
                modValue2 = (7*(ord(lines[index])+ord(lines[ind])))%sizeOfBuckets
                hashTableDict1[modValue1] = hashTableDict1.get(modValue1,0)+1
                hashTableDict2[modValue2] = hashTableDict2.get(modValue2,0)+1


    for element in dictItemCount:
        if(dictItemCount[element] >= support):
                    lstSingleCandidates.append(element)
    
    print(sorted(lstSingleCandidates))
    print(hashTableDict1)
    print(hashTableDict2)
    #Replacing the values of the dictionary by bit maps
    for element in hashTableDict1:
        if(hashTableDict1[element]>= support):
            hashTableDict1[element]=1
        else:
            hashTableDict1[element]=0
    
    for ele in hashTableDict2:
        if(hashTableDict2[ele]>= support):
            hashTableDict2[ele]= 1
        else:
            hashTableDict2[ele]= 0
    
    return sorted(lstSingleCandidates), hashTableDict1, hashTableDict2

if __name__ == '__main__':
    inputData=open(sys.argv[1])
    support = int(sys.argv[2])
    sizeOfBuckets = int(sys.argv[3])
    frequentItemList = []
    hashTableDict1 = {}
    hashTableDict2 = {}
    frequentItemList, hashTableDict1, hashTableDict2=ExecuteFirstPass(inputData, support, sizeOfBuckets)
    inputData.close()
    inputData= open(sys.argv[1])
    ExecuteSecondPass(inputData,frequentItemList, hashTableDict1, hashTableDict2, support, sizeOfBuckets)
