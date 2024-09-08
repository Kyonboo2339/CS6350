import sys
import math
import DataSet
    
def readFile(CSVfile):
    termList = []
    print(CSVfile)
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            termList.append((line.strip().split(',')))        

    return list

#Return heuristic for dataset
def informationGain(labelProportions):
    p_sum = 0
    for label in labelProportions:
        p = labelProportions[label]
        p_sum += p*math.log(p, 2)

    return -1*p_sum


def giniIndex(labelProportions):
    p_sum = 0
    for label in labelProportions:
        p_sum += labelProportions[label]**2

    return 1 - p_sum

def majorityError(labelProportions):
    majorityPercent = float("-inf")
    for label in labelProportions:
        if labelProportions[label] > majorityPercent:
            majorityPercent = labelProportions

    return 1 - majorityPercent

def __main__():
    ID3()
    print("done")

__main__()
#Heuristics

#Information Gain (Entropy)
#Gini Index
#Majority Error
class ID3:
    def __init__(self, heuristic = informationGain):
        self.heuristic = heuristic
        #Read file
        CSVfile = sys.argv[1]
        print(readFile(CSVfile))
        self.data = DataSet(CSVfile)
        #Parse it into formats for the ID3 Algorithm
        #Send into ID3 algorithm
    
    def ID3Algorithm(heuristic = None):
        return None
    
    def calculateGain(self, attributeID):
        setHeuristic = self.heuristic(self.data.labels)
        attributeSum = 0
        attributeProportions = self.data.attributeValueProportions()
        for value in attributeProportions:
            attributeSum += self.heuristic(attributeProportions[value])
            
        return setHeuristic - attributeSum