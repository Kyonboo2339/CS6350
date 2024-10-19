import numpy as np
import sys
import random

class BatchGradient:
    def __init__(self, CSVFile, learningRate):
        self.termList = readFile(CSVFile)
        self.numberOfFeatures = len(self.termList[0]) - 1
        self.outputIndex = len(self.termList[0]) - 1
        self.weights = np.array([0 for i in range(numberOfFeatures)])
        self.learningRate = learningRate
        self.optimizeWeights()

    def testOnFile(self, CSVFile):
        testList = readFile(CSVFile)   
        print(meanSquaredError(testList, self.weights))

    def optimizeWeights(self):
        while True:
            (errorGradient, totalCost) = self.computeGradient()
            newWeight = self.weights - self.learningRate*errorGradient
            if isConverging(self.weights, newWeight):
                break
            
            self.weights = self.weights - self.learningRate*errorGradient
            # print("weights "  + str(self.weights))
            # print("error gradient " + str(errorGradient))
            # print("cost " + str(totalCost))
            # print("error " + str(meanSquaredError(self.termList, self.weights)))

    def computeGradient(self):
        weightgradient = np.array([0 for i in range(numberOfFeatures)])
        totalCost = 0
        for row in self.termList:
            y = row[-1]
            wTx = np.dot(row[:self.numberOfFeatures], self.weights)
            totalCost += y - wTx
            weightgradient = weightgradient + (y - wTx)*row[:self.numberOfFeatures]


        return -1*weightgradient, totalCost
    
class StochasticGradient:
    def __init__(self, CSVFile, learningRate):
        self.termList = readFile(CSVFile)
        self.numberOfFeatures = len(self.termList[0]) - 1
        self.outputIndex = len(self.termList[0]) - 1
        self.weights = np.array([0 for i in range(numberOfFeatures)])
        self.learningRate = learningRate
        self.optimizeWeights()

    def testOnFile(self, CSVFile):
        testList = readFile(CSVFile)   
        print("Error " + str(meanSquaredError(testList, self.weights)))

    def optimizeWeights(self):
        while True:
            errorGradient = self.computeGradient()
            newWeights = self.weights + self.learningRate*errorGradient
            if isConverging(self.weights, newWeights):
                break
            
            self.weights = newWeights

    def computeGradient(self):
        weightgradient = np.array([0 for i in range(numberOfFeatures)])
        randomIndex = random.randint(0, len(self.termList) - 1)
        row = self.termList[randomIndex]
        y = row[-1]
        wTx = np.dot(row[:self.numberOfFeatures], self.weights)

        weightgradient = (y - wTx)*row[:self.numberOfFeatures]


        return weightgradient
    
    
def isConverging(weights, newGradient):
    weightDifference = newGradient - weights
    # print(self.weights)
    # print(newGradient)
    # print("weight difference " + str(weightDifference))
    
    norm = np.linalg.norm(weightDifference)
    #print(norm)
    # print()
    
    return norm < .0000001
    
def meanSquaredError(termList, weights):
    totalError = 0
    for row in termList:
        y = row[-1]
        wTx = np.dot(row[:numberOfFeatures], weights)
        totalError += (y - wTx)**2

    return totalError/2


def readFile(CSVfile):
    termList = []
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            row = line.strip().split(',')
            row.insert(0, 1)
            termList.append([float(feature) for feature in row])        

    return np.array(termList)
    

termList = readFile(sys.argv[1])
numberOfFeatures = len(termList[0]) - 1
outputIndex = len(termList[0]) - 1
weights = np.array([0 for i in range(numberOfFeatures)])

print("batch gradient")
batchGradientDescent = BatchGradient(sys.argv[1], .01)
print(batchGradientDescent.testOnFile(sys.argv[2]))
print(batchGradientDescent.weights)
print()
print("stochastic gradient")
stochasticGradientDescent = StochasticGradient(sys.argv[1], .01)
stochasticGradientDescent.testOnFile(sys.argv[2])
print(stochasticGradientDescent.weights)
