import sys
import Heuristics
import DataSet
    
class ID3Tree:
    def __init__(self, dataSet, heuristic = 'informationGain'):
        if heuristic not in dir(Heuristics):
            raise AttributeError("Heuristic not found")
        
        self.heuristic = getattr(Heuristics, heuristic)
        self.data = dataSet

        self.rootNode = self.ID3(dataSet)
        print(str(self.chooseAttribute(dataSet)))

    def ID3(self, dataSet):
        if dataSet.hasSameLabel():
            return dataSet.mostCommonLabel()
        
        #Create a root node 
        root = self.ID3Node(self.chooseAttribute(dataSet))
        attributeSet = dataSet.attributes[root.attribute]
        for attributeValue in attributeSet:
            subset = dataSet.setSplit(root.attribute, attributeValue)
            if subset.attributeValueDistribution[root.attribute][attributeValue] == 0:
                root.branches[attributeValue] = dataSet.mostCommonLabel()
            else: 
                root.branches[attributeValue] = self.ID3(subset)

        return root

    #Calulate the purity of the set split on a certain attribute
    def calculateGain(self, attributeID, dataSet):
        setHeuristic = self.heuristic(dataSet.labelProportions())
        attributeSum = 0
        attributeProportions = dataSet.attributeValueProportions(attributeID)
        
        for value in attributeProportions:
            attributeWeight = dataSet.attributeValueWeight(attributeID, value)
            attributeSum += attributeWeight*self.heuristic(attributeProportions[value])
            
        return setHeuristic - attributeSum
    
    #Choose the best attribute to split the set
    def chooseAttribute(self, dataSet):
        bestAttribute = None
        maxGain = float("-inf")
        for attributeID in dataSet.attributes:
            attributeGain = self.calculateGain(attributeID, dataSet)
            if attributeGain > maxGain:
                bestAttribute = attributeID
                maxGain = attributeGain
        
        return bestAttribute
    
    #Node for the ID3 tree
    class ID3Node:
        def __init__(self, attribute):
            #Possible values on splitting attribute
            self.branches = {}
            #The attribute the node splits data on
            self.attribute = attribute
     

        

def readFile(CSVfile):
    termList = []
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            termList.append((line.strip().split(',')))        

    return termList
       
def __main__():
    dataSet = DataSet.DataSet(readFile(CSVfile= sys.argv[1]))
    ID3Tree(dataSet, heuristic= sys.argv[2])
    print("done")

__main__()