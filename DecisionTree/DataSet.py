#Manages the counts of each attribute in the set
#Set of attributes
#each attribute has labels 
#data row is placed for each attribute
#self.attributes[attributeID] return a dictionary (attributeValue, dictionary of labels)
#self.attributes[attributeID][attributeValue] returns a dictionary of (label, list of rows with label)
class DataSet():
    def __init__(self, termList):
        self.attributes = {i:{} for i in range(len(termList[0]) - 1)}
        self.labels = {}
        self.Count = len(termList)
        for row in termList:
            label = row[-1]
            for attributeID in range(len(row) - 1):
                attributeValue = row[attributeID]
                attribute = self.attributes[attributeID]

                if attributeValue not in attribute:
                    attribute[attributeValue] = {}

                if label not in attribute[attributeValue]:
                    attribute[attributeValue][label] = []
                
                attribute[attributeValue][label].append(row)
            
            if label not in self.labels:
                self.labels[label] = []
             
            self.labels[label].append(row)

    #Return a new dataSet split on given attributeID and attributeValue
    def setSplit(self, attributeID, attributeValue):
        attributeValue = self.attributes[attributeID][attributeValue]
        dataSetRows = [row for label in attributeValue for row in attributeValue[label]]
        return DataSet(dataSetRows)
    
    #Return percent number of rows for each label for the set
    def labelProportions(self):
        labelCount = {label: sum(len(self.lables[label]))/self.Count for label in self.labels}
        return labelCount
    
    #Returns how many rows have an attribute value given attribute
    def attributeValueCount(self, attributeID):
        attributeValueCount = {value:sum(len(value[label]) for label in value) for value in self.attributes[attributeID]}
        return attributeValueCount
    
    #Returns count of data to label for each attribute value given attribute 
    #rows with attribute value/total rows in set
    def attributeValueProportions(self, attributeID):
        #Number of data in each attribute value
        attributeValueCount = {value:sum(len(value[label]) for label in value) for value in self.attributes[attributeID]}
        #Proportion of label to attribute value
        attributeLabelCount = {value:{label:len(value[label])/attributeValueCount[value] for label in value} for value in self.attributes[attributeID]}
        
        return attributeLabelCount