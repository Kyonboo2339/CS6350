#Manages the counts of each attribute in the set
#self.attributes[attributeID] return a dictionary (attributeValue, dictionary of labels)
#self.attributes[attributeID][attributeValue] returns a dictionary of (label, list of rows with label)
class DataSet():
    def __init__(self, termList, existingAttributes = None, majorityAttributeValues = None, numericThresholds = None, hasNumerics= False, unknownIsMajority= False):
        #Check if there is an existing universe of attribute values.
        if existingAttributes != None:
            self.attributes = {attributeID: {value: {label: [] for label in existingAttributes[attributeID][value]} for value in existingAttributes[attributeID]} for attributeID in existingAttributes}
            self.attributeValueDistribution = {attributeID: {value: 0 for value in existingAttributes[attributeID]} for attributeID in existingAttributes}
            self.numericThresholds = numericThresholds        
            self.majorityAttributes = majorityAttributeValues
        else:
            self.attributes = {i:{} for i in range(len(termList[0]) - 1)}
            if hasNumerics:
                self.numericThresholds = {}
            else:
                self.numericThresholds = None

            if unknownIsMajority:
                self.majorityAttributes = {}
            else:
                self.majorityAttributes = None
            #Tracks how many rows with each attribute value
            self.attributeValueDistribution = {i:{} for i in range(len(termList[0]) - 1)}       
    
        self.labels = {}
        self.unknownMajority = unknownIsMajority
        self.numericAttributes = {0:[], 5:[], 9:[], 11:[], 12:[], 13:[], 14:[]}
        self.hasNumerics = hasNumerics
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
            self.splitNumerics()
         
        #Determine if unknown values should be moved into the majority attribute value
        if unknownIsMajority:
            self.redistributeUnknowns(majorityAttributeValues)
        

        # print(self.numericAttributes)
        
        # print(self.attributeValueDistribution)
                       

    def redistributeUnknowns(self, majorityAttributeValues):
        for attributeID in self.attributes: 
            if 'unknown' in self.attributes[attributeID]:
                    attributeValues = self.attributes[attributeID]["unknown"]
                    unknownRows = [row for label in attributeValues for row in attributeValues[label]]

                    attribute = self.attributes[attributeID]
                    attribute.pop("unknown")
                    self.attributeValueDistribution[attributeID].pop("unknown") 

                    if majorityAttributeValues == None:
                        majorityValue = self.majorityAttributeValue(attributeID)
                    else:
                        majorityValue = self.majorityAttributes[attributeID]
                    
                    for row in unknownRows:
                        attributeValue = attribute[majorityValue]
                        label = row[-1]
                        if label not in attributeValue:
                            attributeValue[label] = []
                
                        attributeValue[label].append(row)

                    self.attributeValueDistribution[attributeID][majorityValue] += len(unknownRows)

                    self.majorityAttributes[attributeID] = majorityValue


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
                    for row in self.attributes[attribute][value][label]:
                        key = 1
                        if int(value) <= median:
                            key = 0
                        
                        valueDistribution[key] += 1

                        if label not in attributeDistribution[key]:
                            attributeDistribution[key][label] = []

                        attributeDistribution[key][label].append(row)
            
            self.attributeValueDistribution[attribute] = valueDistribution
            self.numericThresholds[attribute] = median
            self.attributes[attribute] = attributeDistribution


    #Return a new DataSet split on given attributeID and attributeValue
    def setSplit(self, attributeID, attributeValue):
        if self.hasNumerics and attributeID in self.numericAttributes:
            attributeValue = self.determineNumericValue(attributeID, attributeValue)

        attributeValue = self.attributes[attributeID][attributeValue]
        dataSetRows = [row for label in attributeValue for row in attributeValue[label]]
        return DataSet(dataSetRows, self.attributes, self.majorityAttributes, self.numericThresholds, self.hasNumerics, self.unknownMajority)
    
    def mostCommonLabel(self):
        #print("number of labels " + str(len(self.labels)))
        commonLabel = None
        maxCount = float("-inf")
        for label in self.labels:
            if len(self.labels[label]) > maxCount:
                maxCount = len(self.labels[label])
                commonLabel = label

        if maxCount < 0: return 0 
        return commonLabel
    
    def hasSameLabel(self):
        return len(self.labels) == 1
    
    #Return percentage of rows assigned to each label for the set
    def labelProportions(self):
        #print(str(self.labels["no"]))
        labelCount = {label: len(self.labels[label])/self.Count for label in self.labels}
        return labelCount
    
    #majority value for given attribute
    def majorityAttributeValue(self, attributeID):
        attributeValueCounts = self.attributeValueDistribution[attributeID]
        majorityAttributeValue = None
        maxCount = float("-inf")
       
        for value in attributeValueCounts:
            if value == "unknown": continue
            if attributeValueCounts[value] > maxCount:
                majorityAttributeValue = value
                maxCount = attributeValueCounts[value]

        return majorityAttributeValue
    
    #Returns the percentage of rows with an attribute value 
    def attributeValueWeight(self, attributeID, attributeValue):
        if self.hasNumerics and attributeID in self.numericAttributes:
            attributeValue = self.determineNumericValue(attributeID, attributeValue)

        if self.unknownMajority and attributeValue == "unknown":
            attributeValue = self.majorityAttributeValue(attributeID)

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
                    attributeLabelCount[attributeValue][label] = len(attribute[value][label])/attributeValuesCounts[attributeValue]
                else: 
                    attributeLabelCount[attributeValue][label] = 0

        return attributeLabelCount
    
    def determineNumericValue(self, attributeID, numeric):
        value = 1
        median = self.numericThresholds[attributeID]
        if int(numeric) <= median:
            value = 0

        return value
    
    def isNumericAttribute(self, attributeID):
        return attributeID in self.numericAttributes
    
    def attributeValueTotal(self, attributeID, value):
        if self.hasNumerics and attributeID in self.numericThresholds:
            return self.determineNumericValue(attributeID, value)
        
        return self.attributeValueDistribution[attributeID][value]
    