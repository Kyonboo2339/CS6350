import numpy as np
import sys
from sklearn.utils import shuffle
def readFile(CSVfile):
    termList = []
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            termList.append(np.array((line.strip().split(',')))) 

    termList = np.array(termList).astype(np.float)     
    result = np.hsplit(termList, np.array([3, 5]))
    trainingData = np.append(result[0],  np.full((len(termList), 1), 1), axis= 1)
    print(trainingData)
    labels = np.transpose(result[1])[0]
    labels[labels == 0] = -1
    return trainingData, labels

class SVM:
    def __init__(self, iterations, trainingData, trainLabels, learningRate, a, C, type="standard", learner= "learningRateA"):
        self.predictionType = getattr(SVM, type)
        self.predictor = getattr(SVM, type + "Prediction")
        self.learningRate = getattr(SVM, learner)
        self.iter = iterations
        self.r = learningRate
        self.w = None
        self.C = C
        self.a = a
        self.N = len(trainingData)
        self.predictionType(self, trainingData, trainLabels)

    def standard(self, X, Y):
        w = np.full(len(X[0]), 0.0)

        for i in range(self.iter):
            X, Y = shuffle(X, Y)
            for j in range(3):         
                w = self.update(w, X[i], Y[i], self.learningRate(self, i))
                

        self.w = w
        print("learned weight vector: "  + str(self.w))
    
    def update(self, w, x_i, y_i, learningRate):
       # print(w)
        w_0 = np.append(w[0:len(w) - 1]*learningRate, 0.0)
        
        if y_i*np.dot(w, x_i) <= 1:    
            return w - w_0 + learningRate*self.C*self.N*y_i*x_i 
        else:     
            return w - w_0
    
    def learningRateA(self, t):
        return self.r/(1.0 + t)
    
    def learningRateB(self, t):
        return self.r/(1.0 + (self.r/self.a)*t)

    def testError(self, testData, labels):
        incorrectPred = 0
       
        for i in range(len(testData)):
            if self.predictor(self, testData[i], labels[i]):
                incorrectPred += 1
       
        return incorrectPred/len(testData)
    
    def standardPrediction(self, x, label):
        return np.sign(np.dot(self.w, x)) != label
    
    def isConverging(self, weights, newGradient):
        weightDifference = newGradient - weights
        # print(self.weights)
        # print(newGradient)
        # print("weight difference " + str(weightDifference))
        
        norm = np.linalg.norm(weightDifference)
        #print(norm)
        # print()
        
        return norm < .0000000001
    
    
    

    
    
    
trainingData, trainLabels = readFile(sys.argv[1])
testData, testLabels = readFile(sys.argv[2])
SVMType = sys.argv[3]
iterations = int(sys.argv[4])
learner = "learningRateA"
a = .00001
r = .00001
C = 1


perceptron = SVM(iterations, trainingData, trainLabels, r, a, C, SVMType, learner)
print(SVMType + " Training error: " + str(perceptron.testError(trainingData, trainLabels)))
print(SVMType + " test error: " + str(perceptron.testError(testData, testLabels)))

C = 500/873.0
perceptron = SVM(iterations, trainingData, trainLabels, r, a, C, SVMType, learner)
print(SVMType + " Training error: " + str(perceptron.testError(trainingData, trainLabels)))
print(SVMType + " test error: " + str(perceptron.testError(testData, testLabels)))

C = 700/873.0
perceptron = SVM(iterations, trainingData, trainLabels, r, a, C, SVMType, learner)
print(SVMType + " Training error: " + str(perceptron.testError(trainingData, trainLabels)))
print(SVMType + " test error: " + str(perceptron.testError(testData, testLabels)))

learner = "learningRateB"
a = .00001
r = .0001
print()
print("A___________________________-")
C = 100/873.0
perceptron = SVM(iterations, trainingData, trainLabels, r, a, C, SVMType, learner)
print(SVMType + " Training error: " + str(perceptron.testError(trainingData, trainLabels)))
print(SVMType + " test error: " + str(perceptron.testError(testData, testLabels)))

C = 500/873.0
perceptron = SVM(iterations, trainingData, trainLabels, r, a, C, SVMType, learner)
print(SVMType + " Training error: " + str(perceptron.testError(trainingData, trainLabels)))
print(SVMType + " test error: " + str(perceptron.testError(testData, testLabels)))

C = 700/873.0
perceptron = SVM(iterations, trainingData, trainLabels, r, a, C, SVMType, learner)
print(SVMType + " Training error: " + str(perceptron.testError(trainingData, trainLabels)))
print(SVMType + " test error: " + str(perceptron.testError(testData, testLabels)))