#Manages the counts of each attribute in the set
#self.attributes[attributeID] return a dictionary (attributeValue, dictionary of labels)
#self.attributes[attributeID][attributeValue] returns a dictionary of (label, list of rows with label)
class DataSet():
    def __init__(self, termList, existingAttributes = None):
        #Check if there is an existing universe of attribute values.
        if existingAttributes != None:
            self.attributes = {attributeID: {value: {label: [] for label in existingAttributes[attributeID][value]} for value in existingAttributes[attributeID]} for attributeID in existingAttributes}
            self.attributeValueDistribution = {attributeID: {value: 0 for value in existingAttributes[attributeID]} for attributeID in existingAttributes}
        else:
            self.attributes = {i:{} for i in range(len(termList[0]) - 1)}
            #Tracks how many rows with each attribute value
            self.attributeValueDistribution = {i:{} for i in range(len(termList[0]) - 1)}
            
    
        self.labels = {}
        self.Count = len(termList)
        for row in termList:
            label = row[-1]

            if label not in self.labels:
                self.labels[label] = []
             
            self.labels[label].append(row)

            for attributeID in range(len(row) - 1):
                attributeValue = row[attributeID]
                attribute = self.attributes[attributeID]
                valueDistribution = self.attributeValueDistribution[attributeID]

                if attributeValue not in attribute:
                    attribute[attributeValue] = {}
                    valueDistribution[attributeValue] = 0
                
                valueDistribution[attributeValue] += 1 

                if label not in attribute[attributeValue]:
                    attribute[attributeValue][label] = []
                
                attribute[attributeValue][label].append(row)
    #Return a new DataSet split on given attributeID and attributeValue
    def setSplit(self, attributeID, attributeValue):
        attributeValue = self.attributes[attributeID][attributeValue]
        dataSetRows = [row for label in attributeValue for row in attributeValue[label]]
        return DataSet(dataSetRows, self.attributes)
    
    def mostCommonLabel(self):
        commonLabel = None
        maxCount = float("-inf")
        for label in self.labels:
            if len(self.labels[label]) < maxCount:
                maxCount = len(self.labels[label])
                commonLabel = label
        
        return commonLabel
    
    def hasSameLabel(self):
        return len(self.labels) == 1
    
    #Return percentage of rows assigned to each label for the set
    def labelProportions(self):
        labelCount = {label: len(self.labels[label])/self.Count for label in self.labels}
        return labelCount
    
    #Returns the percentage of rows with an attribute value 
    def attributeValueWeight(self, attributeID, attributeValue):
        return self.attributeValueDistribution[attributeID][attributeValue]/self.Count
    

    #Returns a dict of label distributions based on attribute value subsets
    def attributeValueProportions(self, attributeID):
        #Number of rows in each attribute value
        attributeValueCount = self.attributeValueDistribution[attributeID]
        attribute = self.attributes[attributeID]
        #Proportion of label to attribute value subset
        attributeLabelCount = {value:{label:len(attribute[value][label])/attributeValueCount[value] for label in attribute[value]} for value in attribute}
        
        return attributeLabelCount