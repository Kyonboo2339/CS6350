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
    heuristic = "informationGain"
    depth = -1

    if len(sys.argv) >= 4:
        heuristic = sys.argv[3]
        if len(sys.argv) >= 5:
            depth = int(sys.argv[4])

    trainingFile = readFile(CSVfile= sys.argv[1])
    testFile = readFile(CSVfile= sys.argv[2])

    dataSet = DataSet.DataSet(trainingFile, None, None, True, True)

    if depth == -1:
        depthResults = [] 
        for i in range(1,7):
            decisionTree = ID3.ID3Tree(dataSet, heuristic,  i)
            depthResults.append(results(decisionTree, testFile, trainingFile))
        
        print("\nHeuristic: " + heuristic)
        print("Depth\tTest Error\t\tTraining Error")
        for i in range(6):
            print("  " + str(i + 1) + "\t" + str(depthResults[i][0]) + "\t" + str(depthResults[i][1]))
    else: 
        decisionTree = ID3.ID3Tree(dataSet, heuristic, depth)
        testError, trainingError = results(decisionTree, testFile, trainingFile)
        print("Test Error: " + str(testError) + "  Training Error: " + str(trainingError))

    '''
    Based on the results for car.csv, the training error cannot exceed the test error.
    '''

__main__()