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

def predictOnFile(decisionTree, file= sys.argv[2]):
    testList = readFile(CSVfile= file)
    incorrectPrediction = 0

    for test in testList:
        prediction= decisionTree.predictLabel(test)
        # print("test line: " + str(test))
        # print("prediction: " + str(prediction))
        # print("actual :" + str(test[-1]))
        # print("path taken: " + str(path))
        # print()      
        if prediction != test[-1]:
            incorrectPrediction += 1
    #Determine % error of the decision tree
    print(str(incorrectPrediction) + "/" + str(len(testList)) + " predicted incorrectly")
    print("Error: " + str(incorrectPrediction/len(testList)))

    

    return 
def __main__():
    dataSet = DataSet.DataSet(readFile(CSVfile= sys.argv[1]))
    #Build decision tree
    heuristic = "informationGain"
    if len(sys.argv) == 4:
        heuristic = sys.argv[3]
        
    decisionTree = ID3.ID3Tree(dataSet, heuristic)
    #Read test file
    print("Test Results:" )
    predictOnFile(decisionTree)
    print()
    print("Training Results: ")
    predictOnFile(decisionTree, sys.argv[1])

    print("done")

__main__()