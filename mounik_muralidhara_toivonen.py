# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 16:57:24 2015

@author: mounik
"""

import sys
import re
import random
import itertools

def ExecuteSecondPassToivonen(lstRandomFrequentItemSets, lstNegativeBorderItemSets, lstInputData, support):
        dictFrequentItems= {}
        dictNegativeBorderItemCounts = {}
        lstNegativeBorder= []
        lstFinalFrequentItems = []
        for setItem in lstRandomFrequentItemSets:
            countItem = 0
            for sinList in lstInputData:
                if(set(setItem).issubset(set(sinList))):
                    countItem += 1
            dictFrequentItems[tuple(setItem)] = countItem
            
        for setNegItem in lstNegativeBorderItemSets:
            countNegItem = 0
            for sinLi in lstInputData:
                if(set(setNegItem).issubset(set(sinLi))):
                    countNegItem +=1
            dictNegativeBorderItemCounts[tuple(setNegItem)]=countNegItem
        
        for ele in dictFrequentItems:
            if(dictFrequentItems[ele] >= support):
                lstFinalFrequentItems.append(list(ele))
                
        for elem in dictNegativeBorderItemCounts:
            if(dictNegativeBorderItemCounts[elem] >= support):
                lstNegativeBorder.append(list(elem))
                
        if(len(lstNegativeBorder) == 0):
            performAlgoAgain = 0
        else:
            performAlgoAgain = 1
        
        return performAlgoAgain, lstFinalFrequentItems

def GenerateFrequentRandomItemSets(lstFreqSingleTons, support, maxLengthTransaction, lstInputData, lstNegativeBorderItems):
    lstFreqItems = []
    lstFreqItems = lstFreqSingleTons
    lstFreqAllItems = lstFreqSingleTons
    
    dictCountItemSets = {}
    while(len(lstFreqItems)>0):
        for i in range(maxLengthTransaction):
            for eleInd1 in range(len(lstFreqItems)):
                for eleInd2 in range(eleInd1+1, len(lstFreqItems)):
                    setA = set(lstFreqItems[eleInd1]+lstFreqItems[eleInd2])
                    sortedList = sorted(list(setA))
                    if(len(sortedList) == len(lstFreqItems[eleInd1])+1):
                        count =0
                        for sinTrans in lstInputData:
                            if(set(sortedList).issubset(set(sinTrans))):
                                count += 1
                        dictCountItemSets[tuple(sortedList)] = count
        
        lstFreqItems = []
        for item in dictCountItemSets:
            if(dictCountItemSets[item]>= support):
                lstFreqItems.append(item)
                lstFreqAllItems.append(list(item))
            else:
                lstNegativeBorderItems.append(list(item))
                
        dictCountItemSets.clear()
    
      
    return lstFreqAllItems, lstNegativeBorderItems
    

def AprioriSampleInputData(lstRandInputData, support, fractionOfTransactionUsed):
    dictSingleItemCount = {}
    lstLengthOfLst = []
    lstAllFrequentItem = []
    lstNegativeBorderItems = []
    lstNegativeSingleItems= []
    
    randSupport = int(0.8*fractionOfTransactionUsed*support)
    lstSingleRandFrequentItems = []
    for alist in lstRandInputData:
        lstLengthOfLst.append(len(alist))
        for item in alist:
            dictSingleItemCount[item] = dictSingleItemCount.get(item, 0)+1
            
    for element in dictSingleItemCount:
        if(dictSingleItemCount[element] >= randSupport):
            lstSingleRandFrequentItems.append(list(element))
        else:
            lstNegativeSingleItems.append(list(element))
    
    lstAllFrequentItem,lstNegativeBorderItems=GenerateFrequentRandomItemSets(sorted(lstSingleRandFrequentItems), randSupport, max(lstLengthOfLst), lstRandInputData,lstNegativeSingleItems)
    return lstAllFrequentItem, lstNegativeBorderItems
            

def ExecuteFirstPassToivonen(inputData, support,fractionOfTransactionUsed):
    lstInputData = []
    lstLengthOfEachTrasaction = []
    lstFreqRandItems = []
    lstNegativeBorderItems = []
    
    for line in inputData:
        line = re.findall('\w',line)
        lines = sorted(line)
        lstLengthOfEachTrasaction.append(len(lines))
        lstInputData.append(lines)
    
    
    numberOfElements = len(lstInputData)*fractionOfTransactionUsed
    
    lstRandInputData = random.sample(lstInputData,int(numberOfElements))
    
    lstFreqRandItems, lstNegativeBorderItems = AprioriSampleInputData(lstRandInputData, support, fractionOfTransactionUsed)
    return lstFreqRandItems, lstNegativeBorderItems, lstInputData

if __name__ == '__main__':
    
    inputData=open(sys.argv[1])
    support = int(sys.argv[2])
    
    fractionOfTransactionUsed = 0.4
    numberOfIterations =0
    executeToiven = 1
    lstRandomFrequentItemSets = []
    lstNegativeBorderItemSets = []
    lstFinalFrequentItems = []
    lstInputData= []
    dictSortedList = {}
    while(executeToiven > 0):
        numberOfIterations +=1
        inputData.close()
        inputData=open(sys.argv[1])
        lstRandomFrequentItemSets, lstNegativeBorderItemSets, lstInputData = ExecuteFirstPassToivonen(inputData, support,fractionOfTransactionUsed)
        executeToiven, lstFinalFrequentItems=ExecuteSecondPassToivonen(lstRandomFrequentItemSets, lstNegativeBorderItemSets, lstInputData, support)
    
    print(numberOfIterations)
    print(fractionOfTransactionUsed)
    lstFinalFrequentItems = sorted(lstFinalFrequentItems)
    
    for item in lstFinalFrequentItems:
        dictSortedList.setdefault(len(item),[]).append(item)
    
    for lengthItem in dictSortedList:
        print(list(dictSortedList[lengthItem]))
    
    