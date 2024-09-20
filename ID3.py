import Heuristics
import DataSet
import sys
class ID3Tree:
    def __init__(self, dataSet, heuristic= "informationGain", depthLimit= 6):
        if heuristic not in dir(Heuristics):
            raise AttributeError("Heuristic not found")

        self.heuristic = getattr(Heuristics, heuristic)
        self.data = dataSet
        self.depthLimit = depthLimit
        self.rootNode = self.ID3(dataSet, 0)

    def predictLabel(self, datum):
        currNode = self.rootNode
        while True: 
            # print("Splitting on: " + str(currNode.attribute))
            # print("Branches: " + str(currNode.branches))
            value = datum[currNode.attribute]
            if self.data.hasNumerics and self.data.isNumericAttribute(currNode.attribute):
                value = self.data.determineNumericValue(currNode.attribute, value)

            if self.data.unknownMajority and value == "unknown":
                value = self.data.majorityAttributeValue(currNode.attribute)

            if isinstance(currNode.branches[value], ID3Tree.ID3Node):
                currNode = currNode.branches[value]
            else:
                return currNode.branches[value]

    def ID3(self, dataSet, currDepth):
        if dataSet.hasSameLabel() or currDepth > self.depthLimit:   
            return dataSet.mostCommonLabel()
        
        #Create a root node 
        root = self.ID3Node(self.chooseAttribute(dataSet))
        attributeValues = dataSet.attributes[root.attribute]
        
        for attributeValue in attributeValues:
            subset = dataSet.setSplit(root.attribute, attributeValue)
            if subset.Count == 0:
                root.branches[attributeValue] = dataSet.mostCommonLabel()
            else: 
                root.branches[attributeValue] = self.ID3(subset, currDepth + 1)

        return root

    #Calulate the purity of the set split on a certain attribute
    def calculateGain(self, attributeID, dataSet):
        setHeuristic = self.heuristic(dataSet.labelProportions())
        attributeSum = 0
        attributeProportions = dataSet.attributeValueProportions(attributeID)
        # if attributeID == 14:
        #     print("attribute proportions: " + str(attributeProportions))
        for value in attributeProportions:
            if self.data.unknownMajority and value == "unknown":
                value = self.data.majorityAttributeValue(attributeID)

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



