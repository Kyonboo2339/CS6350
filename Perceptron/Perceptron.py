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
    result = np.hsplit(termList, np.array([4, 6]))
    trainingData = np.append(result[0],  np.full((len(termList), 1), 1), axis= 1)
    labels = np.transpose(result[1])[0]
    labels[labels == 0] = -1
    return trainingData, labels

class Perceptron:
    def __init__(self, iterations, trainingData, trainLabels, learningRate, type="standard"):
        self.predictionType = getattr(Perceptron, type)
        self.predictor = self.predictor = getattr(Perceptron, type + "Prediction")
        self.iter = iterations
        self.r = learningRate
        self.w = None
        self.voted_w_vectors = None
        self.C = None
        self.a = None
        self.predictionType(self, trainingData, trainLabels)

    def standard(self, X, Y):
        w = np.full(len(X[0]), 0)
        for i in range(self.iter):
            X, Y = shuffle(X, Y)
            for i in range(len(X)):
                if Y[i]*np.dot(w, X[i]) <= 0:
                    w = w + self.r*Y[i]*X[i]

        self.w = w
        print("learned weight vector: "  + str(self.w))

    def voted(self, X, Y):
        w = np.full((len(X) + 1,len(X[0])), 0)
        C = np.full(len(X) + 1, 0)
        for n in range(self.iter):
            m = 0
            for i in range(len(X)):
                if Y[i]*np.dot(w[i], X[i]) <= 0:
                    w[m + 1] = w[m] + self.r*Y[i]*X[i]
                    m += 1
                    C[m] = 1
                else:
                    C[m] += 1
                
        self.voted_w_vectors = w
        self.C = C
        print("learned weight vector: "  + str(w))

    def averaged(self, X=None , Y=None):
        w = np.full(len(X[0]), 0)
        a = np.full(len(X[0]), 0)
        for i in range(self.iter):  
            X, Y = shuffle(X, Y)
            for i in range(len(X)):
                if Y[i]*np.dot(w, X[i]) <= 0:
                    w = w + self.r*Y[i]*X[i]
                a = a + w
        
        self.a = a
        print("learned weight vector: "  + str(self.a))
    def testError(self, testData, labels):
        incorrectPred = 0
       
        for i in range(len(testData)):
            if self.predictor(self, testData[i], labels[i]):
                incorrectPred += 1
       
        return incorrectPred/len(testData)
    
    def standardPrediction(self, x, label):
        return np.sign(np.dot(self.w, x)) != label
    
    def averagedPrediction(self, x, label):
        return np.sign(np.dot(self.a, x)) != label
    
    def votedPrediction(self, x, label):
        vote = sum([self.C[i]*np.sign(np.dot(self.voted_w_vectors[i], x)) for i in range(len(self.voted_w_vectors))])
        return np.sign(vote) != label

    
    
    

    
    
    
trainingData, trainLabels = readFile(sys.argv[1])
testData, testLabels = readFile(sys.argv[2])
perceptronType = sys.argv[3]
iterations = int(sys.argv[4])
perceptron = Perceptron(iterations, trainingData, trainLabels, .2, perceptronType)

print(perceptronType + " test error: " + str(perceptron.testError(testData, testLabels)))
