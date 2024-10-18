import Heuristics
import DataSet_W
import sys
class ID3Tree:
    def __init__(self, dataSet, heuristic= "informationGain", depthLimit= 2):
        #print("Created tree~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if heuristic not in dir(Heuristics):
            raise AttributeError("Heuristic not found")

        self.heuristic = getattr(Heuristics, heuristic)
        self.data = dataSet
        self.depthLimit = depthLimit
        self.rootNode = self.ID3(dataSet, 0)
        print("Split on " + str(self.rootNode.attribute))



    def predictLabel(self, datum):
        currNode = self.rootNode
        
        while True: 
            value = datum[currNode.attribute]
            if self.data.hasNumerics and self.data.isNumericAttribute(currNode.attribute):
                value = self.data.determineNumericValue(currNode.attribute, value)

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
        sums = []
        print("attribute: " + str(attributeID))
        for value in attributeProportions:
            #print("value: " + str(value))
            attribute_weighted_average = dataSet.attributeValueWeighted_Average(attributeID, value)
            heuristic = self.heuristic(attributeProportions[value])
            prop = attribute_weighted_average*heuristic
            # print("Weighted Average: " + str(attribute_weighted_average))
            print("proportions " + str(attributeProportions[value]))
            # print("proportions " + str(dataSet.attributes[attributeID][value]))
            # print("gain: " + str(heuristic))
            # print("value prop: " + str(prop))
            # print()
            attributeSum += prop

        print("attribute sum: " + str(attributeSum))
        print("Heuristic " + str(setHeuristic))
        print()
        return setHeuristic - attributeSum
    
    #Choose the best attribute to split the set
    def chooseAttribute(self, dataSet):
        bestAttribute = None
        maxGain = float("-inf")
        attributePurity = []
        for attributeID in dataSet.attributes:
            attributeGain = self.calculateGain(attributeID, dataSet)
            attributePurity.append(attributeGain)
            if attributeGain > maxGain:
                bestAttribute = attributeID
                maxGain = attributeGain

        print("Purity of split " + str(self.calculateGain(bestAttribute, dataSet)))
        print("Purities: " + str(attributePurity))
        print("content " +  str(dataSet.attributeValueDistribution[bestAttribute]))
        return bestAttribute
    
    #Node for the ID3 tree
    class ID3Node:
        def __init__(self, attribute):
            #Possible values on splitting attribute
            self.branches = {}
            #The attribute the node splits data on
            self.attribute = attribute



