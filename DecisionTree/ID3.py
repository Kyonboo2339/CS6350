import Heuristics
import DataSet
import sys
class ID3Tree:
    def __init__(self, dataSet, heuristic = 'informationGain', depthLimit = 6):
        if heuristic not in dir(Heuristics):
            raise AttributeError("Heuristic not found")
        
        self.heuristic = getattr(Heuristics, heuristic)
        self.data = dataSet
        self.depthLimit = depthLimit
        self.rootNode = self.ID3(dataSet, 0)
        #self.rootNode.preorder()

    def predictLabel(self, datum):
        currNode = self.rootNode
        while True: 
            value = datum[currNode.attribute]
            if isinstance(currNode.branches[value], ID3Tree.ID3Node):
                currNode = currNode.branches[value]
            else:
                return currNode.branches[value]

    def ID3(self, dataSet, currDepth):
        if dataSet.hasSameLabel() or currDepth >= self.depthLimit:
            return dataSet.mostCommonLabel()
        
        #Create a root node 
        root = self.ID3Node(self.chooseAttribute(dataSet))
        attributeValues = dataSet.attributes[root.attribute]
        for attributeValue in attributeValues:
            subset = dataSet.setSplit(root.attribute, attributeValue)
            if subset.attributeValueDistribution[root.attribute][attributeValue] == 0:
                root.branches[attributeValue] = dataSet.mostCommonLabel()
            else: 
                root.branches[attributeValue] = self.ID3(subset, currDepth + 1)

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

        def preorder(self):
            print(str(self.attribute))
            

            for branch in self.branches:
                if isinstance(self.branches[branch], ID3Tree.ID3Node):
                    print(self.branches[branch].preorder())



