import ID3
import DataSet_W
import sys
import Adaboost

def readFile(CSVfile):
    termList = []
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        rowNumber = 0
        for line in file:
            termList.append((rowNumber, line.strip().split(',')))        
            rowNumber += 1
    return termList

def predictOnFile(decisionTree, testList):
    incorrectPrediction = 0

    for test in testList:
        prediction= decisionTree.predictLabel(test)     
        if prediction != test[-1]:
            incorrectPrediction += 1

    return str(incorrectPrediction/len(testList))

def results(decisionTree, testFile, trainingFile):
    #Read test file
    testError = predictOnFile(decisionTree, testFile)
    trainingError = predictOnFile(decisionTree, trainingFile)
    return testError, trainingError

def __main__():    
    #Build decision tree

    trainingFile_bank = readFile(sys.argv[1])
    testFile_bank = readFile(sys.argv[2])

    #dataSet_bank_unknown = DataSet_W.DataSet(trainingFile_bank, None, None, None, False, None)
    #Look at using wrong proportions. entrpy needs to be based on the labels. not the values
    adaboost = Adaboost.Adaboost(sys.argv[1], 2)

    print("test Error " + str(adaboost.predictOnFile(testFile_bank)))

    
    '''
    Based on the results for car.csv, the training error cannot exceed the test error.
    '''

__main__()