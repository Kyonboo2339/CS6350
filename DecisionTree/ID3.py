import sys
import Heuristics
import DataSet
    
def readFile(CSVfile):
    termList = []
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            termList.append((line.strip().split(',')))        

    return termList
    
class ID3:
    def __init__(self, dataSet, heuristic = 'informationGain'):
        if heuristic not in dir(Heuristics):
            raise AttributeError("Heuristic not found")
        
        self.heuristic = getattr(Heuristics, heuristic)
        #Read file
        self.data = dataSet
        print(str(self.chooseAttribute()))
        #Parse it into formats for the ID3 Algorithm
        #Send into ID3 algorithm
    
    def ID3Algorithm(heuristic = None):
        return None
    
    #Calulate the purity of the set split on a certain attribute
    def calculateGain(self, attributeID):
        setHeuristic = self.heuristic(self.data.labelProportions())
        attributeSum = 0
        attributeProportions = self.data.attributeValueProportions(attributeID)
        
        for value in attributeProportions:
            attributeWeight = self.data.attributeValueWeight(attributeID, value)
            attributeSum += attributeWeight*self.heuristic(attributeProportions[value])
            
        return setHeuristic - attributeSum
    
    #Choose the best attribute to split the set
    def chooseAttribute(self):
        bestAttribute = None
        maxGain = float("-inf")
        for attributeID in self.data.attributes:
            attributeGain = self.calculateGain(attributeID)
            if attributeGain > maxGain:
                bestAttribute = attributeID
                maxGain = attributeGain
        
        return bestAttribute

    #Node for the ID3 tree
    class Node:
        def __init__(self):
            return None
        
def __main__() :
    CSVfile = sys.argv[1]  
    dataSet = DataSet.DataSet(readFile(CSVfile))
    ID3(dataSet, sys.argv[2])
    print("done")

__main__()