import numpy as np
import sys
import scipy.optimize as sp
from sklearn.utils import shuffle
def readFile(CSVfile):
    termList = []
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            termList.append(np.array((line.strip().split(',')))) 

    termList = np.array(termList).astype(np.float)     
    result = np.hsplit(termList, np.array([4, 6]))
    trainingData = result[0]#np.append(result[0],  np.full((len(termList), 1), 1), axis= 1)
    
    labels = np.transpose(result[1])[0]
    labels[labels == 0] = -1
    return trainingData, labels

class DualSVM:
    def __init__(self, trainingData, trainLabels, C, lambda_):
        self.w = None
        self.b = None
        self.C = C
        self.lamba_ = lambda_
        self.X = trainingData
        self.Y = trainLabels
        self.a = None
        self.N = len(trainingData)
        self.xTx_list = []
        self.y_list = []
        #self.memoizeX()
        self.memoizeY()
        self.gaussianKernel()
        self.optimize_w()
        
    def optimize_w(self):
        a_start = np.full(len(self.X), 0.0)
        print("in optimize")
        b = (0, self.C)
        bnds = [b for i in range(len(a_start))]
        a = sp.minimize(self.DualSVMFunction, a_start, method= "SLSQP", bounds=bnds)
        #print(a.x)
        optimized_a = np.array(a.x)
        self.a = optimized_a
        self.w = np.sum((self.Y*optimized_a*self.X.T).T, axis=0)
        self.b = self.find_b(self.w)
        #
        # print(self.w)
    

    def DualSVMFunction(self, a):
        sum_a = np.sum(a)       
        sum = np.sum(np.array([np.sum((self.y_list[i])*(a[i]*a)*(self.xTx_list[i])) for i in range(len(self.X))]))*.5

        return sum - sum_a
    
    def memoizeX(self):
        for i in range(len(self.X)):
            self.xTx_list.append(np.sum(self.X[i]*self.X,axis=1))

    def gaussianKernel(self):
        for i in range(len(self.X)):
            kernel = []
            for j in range(len(self.X)):
                kernel.append(self.gaussian(self.X[i], self.X[j]))
            self.xTx_list.append(np.sum(np.array(kernel)))
    
    def gaussian(self, w_i, w_j):
        dist = np.linalg.norm(w_i - w_j)**2
        return np.exp(-1*dist/self.lamba_)

    def memoizeY(self):
        for i in range(len(self.X)):
            self.y_list.append((self.Y[i]*self.Y))


    def find_b(self, w):
        b = np.sum(self.Y - np.sum(w*self.X, axis= 1))/len(self.Y)
        return b

    def testError(self, testData, labels):
        incorrectPred = 0
       
        for i in range(len(testData)):
            if self.kernelPredict(testData[i], labels[i]):
                incorrectPred += 1
       
        return incorrectPred/len(testData)
    
    def standardPrediction(self, x, label):
        return np.sign(np.dot(self.w, x)) != label
    
    def kernelPredict(self, x, label):
        ay = self.a*self.Y
        wTx = np.sum(ay*np.array([self.gaussian(x_i, x) for x_i in self.X])) + self.b
        return np.sign(wTx) != label

    

    
    
    
trainingData, trainLabels = readFile(sys.argv[1])
testData, testLabels = readFile(sys.argv[2])

learningRates = [.1, .5, 1, 5, 100]
C = [100/873.0, 500/873.0, 700/873.0]

for c in C:
    for rate in learningRates:
        dualSVM = DualSVM(trainingData, trainLabels, c, rate)
        print("C = " + str(c))
        print("lambda = " + str(rate))
        print(" Training error: " + str(dualSVM.testError(trainingData, trainLabels)))
        print(" test error: " + str(dualSVM.testError(testData, testLabels)))
# print (trainingData)
# learner = "learningRateA"

# C = 100/873.0
# dualSVM = DualSVM(trainingData, trainLabels, C)
# print(" Training error: " + str(dualSVM.testError(trainingData, trainLabels)))
# print(" test error: " + str(dualSVM.testError(testData, testLabels)))

# C = 500/873.0
# dualSVM = DualSVM(trainingData, trainLabels, C)
# print(" Training error: " + str(dualSVM.testError(trainingData, trainLabels)))
# print(" test error: " + str(dualSVM.testError(testData, testLabels)))

# C = 700/873.0
# dualSVM = DualSVM(trainingData, trainLabels, C)
# print(" Training error: " + str(dualSVM.testError(trainingData, trainLabels)))
# print(" test error: " + str(dualSVM.testError(testData, testLabels)))
