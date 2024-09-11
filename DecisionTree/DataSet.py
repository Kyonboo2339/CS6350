#Manages the counts of each attribute in the set
#self.attributes[attributeID] return a dictionary (attributeValue, dictionary of labels)
#self.attributes[attributeID][attributeValue] returns a dictionary of (label, list of rows with label)
class DataSet():
    def __init__(self, termList, existingAttributes = None, numericThresholds = None, hasNumerics= False, unknownIsMajority= False):
        #Check if there is an existing universe of attribute values.
        if existingAttributes != None:
            self.attributes = {attributeID: {value: {label: [] for label in existingAttributes[attributeID][value]} for value in existingAttributes[attributeID]} for attributeID in existingAttributes}
            self.attributeValueDistribution = {attributeID: {value: 0 for value in existingAttributes[attributeID]} for attributeID in existingAttributes}
            self.numericThresholds = numericThresholds         
        else:
            self.attributes = {i:{} for i in range(len(termList[0]) - 1)}
            self.numericThresholds = {}
            #Tracks how many rows with each attribute value
            self.attributeValueDistribution = {i:{} for i in range(len(termList[0]) - 1)}       
    
        self.labels = {}
        self.numericAttributes = {0:[], 5:[], 9:[], 11:[], 12:[], 13:[], 14:[]}
        self.Count = len(termList)
        #Fill structures will information from read file
        for row in termList:
            label = row[-1]

            if label not in self.labels:
                self.labels[label] = []
             
            self.labels[label].append(row)

            for attributeID in range(len(row) - 1):
                
                attributeValue = row[attributeID]
                attribute = self.attributes[attributeID]
                valueDistribution = self.attributeValueDistribution[attributeID]

                if hasNumerics and numericThresholds == None and attributeID in self.numericAttributes:
                    self.numericAttributes[attributeID].append(int(attributeValue))

                if attributeValue not in attribute:
                    attribute[attributeValue] = {}
                    valueDistribution[attributeValue] = 0
                
                valueDistribution[attributeValue] += 1 

                if label not in attribute[attributeValue]:
                    attribute[attributeValue][label] = []
                
                attribute[attributeValue][label].append(row)

        #Splitting numeric attribute values by median 
        if hasNumerics:
            for attribute in self.numericAttributes:
                self.numericAttributes[attribute].sort()
                sortedValues = self.numericAttributes[attribute]

                median = int(sortedValues[int(len(sortedValues)/2)])                
                valueDistribution = {0:0, 1:0}

                for value in self.numericAttributes[attribute]:
                    key = 1
                    if value <= median:
                        key = 0
                    
                    valueDistribution[key] += 1
                
                self.attributeValueDistribution[attribute] = valueDistribution
                self.numericThresholds[attribute] = median
        
        #Determine if unknown values should be moved into the majority attribute value
        if unknownIsMajority:
            print("redistributing unknowns")
            for attributeID in self.attributes: 
                if attributeID not in self.numericAttributes and 'unknown' in self.attributes[attributeID]:
                    #print(str(self.attributes[attributeID]))
                    attributeValues = self.attributes[attributeID]["unknown"]
                    unknownRows = [row for label in attributeValues for row in attributeValues[label]]

                    attribute = self.attributes[attributeID]
                    attribute.pop("unknown")
                    self.attributeValueDistribution[attributeID].pop("unknown") 
                    majorityValue = self.majorityAttributeValue(attributeID)
                    
                    for row in unknownRows:
                        attributeValue = attribute[majorityValue]
                        if label not in attributeValue:
                            attributeValue[label] = []
                
                        attributeValue[label].append(row)

                    self.attributeValueDistribution[attributeID][majorityValue] += len(unknownRows)


        #print(str(self.attributeValueDistribution))              

    #Return a new DataSet split on given attributeID and attributeValue
    def setSplit(self, attributeID, attributeValue):
        attributeValue = self.attributes[attributeID][attributeValue]
        dataSetRows = [row for label in attributeValue for row in attributeValue[label]]
        return DataSet(dataSetRows, self.attributes, self.numericThresholds)
    
    def mostCommonLabel(self):
        #print("number of labels " + str(len(self.labels)))
        commonLabel = None
        maxCount = float("-inf")
        for label in self.labels:
            if len(self.labels[label]) > maxCount:
                maxCount = len(self.labels[label])
                commonLabel = label
              
        return commonLabel
    
    def hasSameLabel(self):
        return len(self.labels) == 1
    
    #Return percentage of rows assigned to each label for the set
    def labelProportions(self):
        labelCount = {label: len(self.labels[label])/self.Count for label in self.labels}
        return labelCount
    
    #majority value for given attribute
    def majorityAttributeValue(self, attributeID):
        attributeValueCounts = self.attributeValueDistribution[attributeID]
        majorityAttributeValue = None
        maxCount = float("-inf")
        #print(str(attributeValueCounts))
        for value in attributeValueCounts:
            print("value: " + value)
            if attributeValueCounts[value] == "unknown": continue
                
            if attributeValueCounts[value] > maxCount:
                majorityAttributeValue = value
                maxCount = attributeValueCounts[value]
        
        return majorityAttributeValue
    
    #Returns the percentage of rows with an attribute value 
    def attributeValueWeight(self, attributeID, attributeValue):
        return self.attributeValueDistribution[attributeID][attributeValue]/self.Count
    

    #Returns a dict of label distributions based on attribute value subsets
    def attributeValueProportions(self, attributeID):
        #Number of rows in each attribute value
        attributeValuesCounts = self.attributeValueDistribution[attributeID]
        attribute = self.attributes[attributeID]

        #Proportion of label to attribute value subset
        attributeLabelCount = {}
        for value in attribute:
            attributeLabelCount[value] = {}
            for label in attribute[value]:
                attributeLabelCount[value][label] = None
                if attributeValuesCounts[value] > 0:
                    attributeLabelCount[value][label] = len(attribute[value][label])/attributeValuesCounts[value]
                else: 
                    attributeLabelCount[value][label] = 0
    
        return attributeLabelCount