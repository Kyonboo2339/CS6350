import ID3 
import DataSet_W
import sys
import math
class Adaboost:
    def __init__(self, CSVfile, iterations):
        self.trainingFile = self.readFile(CSVfile)
        D_weights = {i: 1/len(self.trainingFile) for i in range(len(self.trainingFile))}
        self.dataSet_bank_unknown = DataSet_W.DataSet(self.trainingFile, None, None, None, True, D_weights)
        self.predictions = []
        self.classifiersAndVotes = []
        heuristic = "informationGain"

        

        for iteration in range(iterations):
            print("Tree " + str(iteration) +": ")
            weakDecisionTree = ID3.ID3Tree(self.dataSet_bank_unknown, heuristic, 1)
            print(self.dataSet_bank_unknown.attributeValueDistribution[0])
            trainingError = self.calculateTrainingError(weakDecisionTree)
            print("Number of rows wrong : " + str(self.predictions.count(-1)))
            print("Training Error: " + str(trainingError))
            self.classifiersAndVotes.append((weakDecisionTree, self.calculateAlpha(trainingError)))
            self.constructD_weights(trainingError)
            print()
            
            # maxWeight = 0 
            # for weight in new_D_weights:
            #     maxWeight = max(maxWeight, new_D_weights[weight])

            # print("Max weight " + str(maxWeight))
        print("Number of tree created: " + str(len(self.classifiersAndVotes)))
        # for i in range(iterations):
        #     print("Tree " + str(i) + " weights")


    

    def readFile(self, CSVfile):
        termList = []
        #Basic line reading. Need to sort by label
        with open(CSVfile, 'r') as file:
            rowNumber = 0
            for line in file:
                termList.append((rowNumber, (line.strip().split(','))))        
                rowNumber += 1
        return termList
    
    def predictOnFile(self, testList):
        incorrectPrediction = 0

        for rowNumber, testRow in testList:  
            prediction = self.checkPrediction(testRow)
            
            if prediction != testRow[-1]:
                incorrectPrediction += 1
                print("Row " + str(rowNumber) + " Expected : " + prediction + "    Test: " + testRow[-1] )

        return str(incorrectPrediction/len(testList))

    def checkPrediction(self, testRow):
        predictionSum = 0

        actual = testRow[-1]
        for classifier, vote in self.classifiersAndVotes:
            predictionSum += vote*self.prediction(classifier.predictLabel(testRow))
        
        #print("Prediction sum: " + str(predictionSum))

        if predictionSum < 0:
            return "no"
        return "yes"
    
    def prediction(self, hypothesis):
        if hypothesis == "no":
            return -1 
        else:
            return 1

    def calculateTrainingError(self, decisionTree):
        incorrectPrediction = 0
        for rowTuple in self.trainingFile:
            row = rowTuple[1]
            rowNumber = rowTuple[0]
            prediction = decisionTree.predictLabel(row)     
            if prediction != row[-1]:
                incorrectPrediction += self.dataSet_bank_unknown.D_weights[rowNumber]
                #print("error weight: " + str(self.dataSet_bank_unknown.D_weights[rowNumber]))
                print("Row " + str(rowNumber) + " Expected : " + prediction + "    Test: " + row[-1] )
                self.predictions.append(-1)
            else:
                self.predictions.append(1)


        
        return incorrectPrediction/1.0
    
    def calculateAlpha(self, trainingError):
        if trainingError == 0:
            return 0
        
        alpha = .5*math.log((1.0 - trainingError) / trainingError)
        return alpha
    
    def constructD_weights(self, trainingError):
        print(self.dataSet_bank_unknown.attributeValueDistribution[0])
        D_weights_prev = self.dataSet_bank_unknown.D_weights
        D_weights_next = {i: 0 for i in range(len(D_weights_prev))}
        alpha = self.calculateAlpha(trainingError)
        normalization = 2*math.sqrt((1-trainingError)*trainingError)
        sum = 0 
        #Calculate the weights for t + 1
        for i in range(len(D_weights_prev)):
            e = math.exp((-1.0)*alpha*self.predictions[i])
            D_weights_next[i] = D_weights_prev[i]*e/normalization
            sum += D_weights_next[i]
        #print("Normalization" + str(normalization))
        #Normalize
        #Clear predictions for the calculations of training error
        self.predictions.clear()

        print("sum " + str(sum))
        self.dataSet_bank_unknown.D_weights = D_weights_next
        self.dataSet_bank_unknown.updateAttributeDistribution()


