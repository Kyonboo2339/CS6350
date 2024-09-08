import sys
import csv

class ID3:
    def __init__(self):
        #Read file
        CSVfile = sys.argv[1]
        print(readFile(CSVfile))
        #Parse it into formats for the ID3 Algorithm
        #Send into ID3 algorithm
        
    
def readFile(CSVfile):
    termList = []
    print(CSVfile)
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            termList.append((line.strip().split(',')))        

    return list

#Manages the counts of each attribute in the set
#Set of attributes
#each attribute has labels 
#data row is placed for each attribute
#self.attributes[attributeID] return a dictionary (attributeValue, dictionary of labels)
#self.attributes[attributeID][attributeValue] returns a dictionary of (label, list of rows with label)
class dataSet():
    def __init__(self, termList):
        self.attributes = {i:{} for i in range(len(termList[0]) - 1)}
        self.labels = {}
        self.dataCount = len(termList)
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

    #Return data split on certain attribute
    def setSplit(self, attributeID):
        return self.attributes[attributeID]
    
    #Returns proportion of data to label for each attribute value given attribute 
    def attributeValueProportions(self, attributeID):
        #Number of data in each attribute value
        attributeValueCount = {value:sum(len(value[label]) for label in value) for value in self.attributes[attributeID]}
        #Proportion of label to attribute value
        attributeLabelCount = {value:{label:len(value[label])/attributeValueCount[value] for label in value} for value in self.attributes[attributeID]}
        
        return attributeLabelCount

def __main__():
    ID3()
    print("done")

__main__()
#Heuristics
#Information Gain (Entropy)
#Gini Index
#Majority Error