import ID3
import DataSet
import sys

def readFile(CSVfile):
    termList = []
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            termList.append((line.strip().split(',')))        

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

    trainingFile_car = readFile(CSVfile= sys.argv[1])
    testFile_car = readFile(CSVfile= sys.argv[2])
    trainingFile_bank = readFile(sys.argv[3])
    testFile_bank = readFile(sys.argv[4])

    dataSet_car = DataSet.DataSet(trainingFile_car, None, None, False, False)
    dataSet_bank_unknown = DataSet.DataSet(trainingFile_bank, None, None, True, False)
    dataSet_bank_unknownMajority = DataSet.DataSet(trainingFile_bank, None, None, True, True)
    heuristics = ["informationGain", "giniIndex", "majorityError"]
    print("Car results:\n")
     
    for heuristic in heuristics:
        depthResults = []
        for i in range(1,7):
            decisionTree = ID3.ID3Tree(dataSet_car, heuristic,  i)
            depthResults.append(results(decisionTree, testFile_car, trainingFile_car))
        print("\nHeuristic: " + heuristic)
        print("Depth\tTest Error\t\tTraining Error")
        for i in range(6):
            print("  " + str(i + 1) + "\t" + str(depthResults[i][0]) + "\t" + str(depthResults[i][1]))

    print("\nResults for bank, unknown is attribute:")

    for heuristic in heuristics:
        depthResults = []
        for i in range(1,17):
            decisionTree = ID3.ID3Tree(dataSet_bank_unknown, heuristic,  i)
            depthResults.append(results(decisionTree, testFile_bank, trainingFile_bank))
        print("\nHeuristic: " + heuristic)
        print("Depth\tTest Error\tTraining Error")
        for i in range(16):
            print("  " + str(i + 1) + "\t" + str(depthResults[i][0]) + "\t\t" + str(depthResults[i][1]))

    print("\nResults for bank, unknown is majority:")

    for heuristic in heuristics:
        depthResults = []
        for i in range(1,17):
            decisionTree = ID3.ID3Tree(dataSet_bank_unknownMajority, heuristic,  i)
            depthResults.append(results(decisionTree, testFile_bank, trainingFile_bank))
        print("\nHeuristic: " + heuristic)
        print("Depth\tTest Error\tTraining Error")
        for i in range(16):
            print("  " + str(i + 1) + "\t" + str(depthResults[i][0]) + "\t\t" + str(depthResults[i][1]))
            
    '''
    Based on the results for car.csv, the training error cannot exceed the test error.
    '''

__main__()