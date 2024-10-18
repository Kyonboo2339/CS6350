#Manages the counts of each attribute in the set
#self.attributes[attributeID] return a dictionary (attributeValue, dictionary of labels)
#self.attributes[attributeID][attributeValue] returns a dictionary of (label, list of rows with label)
class DataSet():
    def __init__(self, termList, existingAttributes = None, majorityAttributeValues = None, numericThresholds = None, hasNumerics= False, D_weights = None):
        #Check if there is an existing universe of attribute values.
        #print("Created new dataset~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if existingAttributes != None:
            self.attributes = {attributeID: {value: {label: [] for label in existingAttributes[attributeID][value]} for value in existingAttributes[attributeID]} for attributeID in existingAttributes}
            self.attributeValueDistribution = {attributeID: {value: 0 for value in existingAttributes[attributeID]} for attributeID in existingAttributes}
            self.numericThresholds = numericThresholds        
            self.majorityAttributes = majorityAttributeValues
            self.D_weights = D_weights
        else:
            self.attributes = {i:{} for i in range(len(termList[0][1]) - 1)}
            #Tracks how many rows with each attribute value
            self.attributeValueDistribution = {i:{} for i in range(len(termList[0][1]) - 1)}  
            self.D_weights = None
            self.numericThresholds = None
            self.majorityAttributes = None

            if hasNumerics:
                self.numericThresholds = {}

            if D_weights == None:
                self.D_weights = {i: 1/len(termList) for i in range(len(termList))}
            else:
                self.D_weights = D_weights
                
                 
    
        self.labels = {}
        self.numericAttributes = {0:[], 5:[], 9:[], 11:[], 12:[], 13:[], 14:[]}
        self.hasNumerics = hasNumerics
        self.Count = 0
        #self.rowSums = {attribute: {} for attribute in range(len(termList))}
        
        #Fill structures will information from read file
        for rowTuple in termList:
            rowNumber, row = rowTuple
            label = row[-1]

            self.Count += self.D_weights[rowNumber]

            if label not in self.labels:
                self.labels[label] = []
             
            self.labels[label].append(rowTuple)

            for attributeID in range(len(row) - 1):
                attributeValue = row[attributeID]
                attribute = self.attributes[attributeID]
                valueDistribution = self.attributeValueDistribution[attributeID]

                if hasNumerics and numericThresholds == None and attributeID in self.numericAttributes:
                    self.numericAttributes[attributeID].append(int(attributeValue))

                if attributeValue not in attribute:
                    attribute[attributeValue] = {}
                    valueDistribution[attributeValue] = 0
                
                
                valueDistribution[attributeValue] += self.D_weights[rowNumber]

                if label not in attribute[attributeValue]:
                    attribute[attributeValue][label] = []
                
                attribute[attributeValue][label].append(rowTuple)
      

        
        #Splitting numeric attribute values by median 
        if hasNumerics:
            self.splitNumerics()

        #print(self.attributeValueDistribution[15]["unknown"])
    #Distributes numeric values into binary groups. greater than less than median
    def splitNumerics(self):
        for attribute in self.numericAttributes:
            self.numericAttributes[attribute].sort()
            sortedValues = self.numericAttributes[attribute]
            
            if len(self.numericThresholds) != len(self.numericAttributes):
                median = int(sortedValues[int(len(sortedValues)/2)])  
            else:
                median = self.numericThresholds[attribute]     

            valueDistribution = {0:0, 1:0}
            attributeDistribution = {0:{}, 1:{}}

            for value in self.attributes[attribute]:
                for label in self.attributes[attribute][value]:
                    for rowTuple in self.attributes[attribute][value][label]:
                        key = 1
                        if int(value) <= median:
                            key = 0
                        
                        if label not in attributeDistribution[key]:
                            attributeDistribution[key][label] = []

                        rowWeight = self.D_weights[rowTuple[0]]

                        valueDistribution[key] += rowWeight

                        attributeDistribution[key][label].append(rowTuple)
            
            self.attributeValueDistribution[attribute] = valueDistribution
            self.numericThresholds[attribute] = median
            self.attributes[attribute] = attributeDistribution


    #Return a new DataSet split on given attributeID and attributeValue
    def setSplit(self, attributeID, attributeValue):
        if self.hasNumerics and attributeID in self.numericAttributes:
            attributeValue = self.determineNumericValue(attributeID, attributeValue)

        attributeValue = self.attributes[attributeID][attributeValue]
        dataSetRows = [rowTuple for label in attributeValue for rowTuple in attributeValue[label]]
        return DataSet(dataSetRows, self.attributes, self.majorityAttributes, self.numericThresholds, self.hasNumerics, self.D_weights)
    
    def mostCommonLabel(self):
        #print("number of labels " + str(len(self.labels)))
        commonLabel = None
        maxCount = float("-inf")
        for label in self.labels:
            labelCount = self.rowsSum(self.labels[label])
            if labelCount > maxCount:
                maxCount = labelCount
                commonLabel = label

        if maxCount < 0: return 0 
        return commonLabel
    
    def hasSameLabel(self):
        return len(self.labels) == 1
    
    #Return percentage of rows assigned to each label for the set
    def labelProportions(self):
        #print(str(self.labels["no"])
        
        labelCount = {label: self.rowsSum(self.labels[label])/self.Count for label in self.labels}
        print("Labels: " + str(labelCount))
       
        return labelCount
    
    #Returns the percentage of rows with an attribute value 
    def attributeValueWeighted_Average(self, attributeID, attributeValue):
        if self.hasNumerics and attributeID in self.numericAttributes:
            attributeValue = self.determineNumericValue(attributeID, attributeValue)

        return self.attributeValueDistribution[attributeID][attributeValue]/self.Count
    

    #Returns a dict of label distributions based on attribute value subsets
    def attributeValueProportions(self, attributeID):
        
        #Number of rows in each attribute value
        attributeValuesCounts = self.attributeValueDistribution[attributeID]
        attribute = self.attributes[attributeID]

        #Proportion of label to attribute value subset
        attributeLabelCount = {}

        for value in attribute:
            attributeValue = value

            attributeLabelCount[attributeValue] = {}
            for label in attribute[value]:
                attributeLabelCount[attributeValue][label] = None

                if attributeValuesCounts[attributeValue] > 0:
                    prop = self.rowsSum(attribute[value][label])/attributeValuesCounts[attributeValue]

                    attributeLabelCount[attributeValue][label] = self.rowsSum(attribute[value][label])/attributeValuesCounts[attributeValue]
                else: 
                    attributeLabelCount[attributeValue][label] = 0

      
        return attributeLabelCount
    
    #Returns a weighted total of labels
    
    def determineNumericValue(self, attributeID, numeric):
        value = 1
        median = self.numericThresholds[attributeID]
        if int(numeric) <= median:
            value = 0

        return value
    
    def rowsSum(self, rowTuples):
        labelTotal = 0
        for rowTuple in rowTuples:
            labelTotal += self.D_weights[rowTuple[0]]

        return labelTotal

    def isNumericAttribute(self, attributeID):
        return attributeID in self.numericAttributes
    
    
    def updateAttributeDistribution(self):
        for attributeID in self.attributes:
            print(attributeID)
            print("before")
            print(self.attributeValueDistribution[attributeID])
            for value in self.attributes[attributeID]:

                valueSum = 0
            
                for label in self.attributes[attributeID][value]:
                    for rowNumber, row in self.attributes[attributeID][value][label]:
                        valueSum += self.D_weights[rowNumber]

                self.attributeValueDistribution[attributeID][value] = valueSum 
            print("after")
            print(self.attributeValueDistribution[attributeID])
            print()