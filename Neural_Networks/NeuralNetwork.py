import pandas as pd
import sys
from sklearn.utils import shuffle
import math
import numpy as np

class NeuralNetwork:

    def __init__(self, featureData, labels, hidden_layer_width, layer_1_weights, layer_2_weights, layer_3_weights, numEpochs, learningRate_func, init_r, d):
        self.layer_width = hidden_layer_width
        self.X = featureData
        self.Y = labels
        self.r = learningRate_func
        self.r_0 = init_r
        self.y = 0
        self.sigmoid = np.vectorize(self.sigmoid_func)
        self.epoch = numEpochs
        self.d = d

        #x to z1
        self.layer_1 = layer_1_weights[0:,1:]
        self.bias_layer_1 = layer_1_weights[0:,0:1]
        self.deriv_1 = None
        self.bias_deriv_1 = None
        self.z1 = None

        #z1 to z2
        self.layer_2 = layer_2_weights[0:,1:]
        self.bias_layer_2 = layer_2_weights[0:,0:1]
        self.deriv_2 = None
        self.bias_deriv_2 = None
        self.z2 = None

        #z3 to y

        self.layer_3 = layer_3_weights[0:, 1:]
        self.deriv_3 = None
        self.bias_deriv_3 = None
        self.bias_layer_3 = layer_3_weights[0:, 0:1]
    

    def forwardPass(self, x):
        #updating layer 1 
        self.z1 = self.sigmoid(np.sum(self.layer_1*x,axis= 1, keepdims=True) + self.bias_layer_1)
        #updating layer 2
        self.z2 = self.sigmoid(np.sum(self.layer_2.T*self.z1.T, axis= 0, keepdims=True).T + self.bias_layer_2)
        self.z2 = self.z2.T
        #y output
        y_pred = np.sum(self.layer_3*self.z2, axis= 1) + self.bias_layer_3

        return np.sign(y_pred)
        
    

    def backwardsPass(self, y, y_pred, x):
        deriv_loss = y - y_pred
        #update weights between y and z2
        self.deriv_3 = deriv_loss*self.z2
        self.bias_deriv_3 = deriv_loss

        #update weights between z1 and z2
        #deriv = loss*w_i*z2_i*(1 - z2_i)*z1
        loss_layer_2 = deriv_loss*self.layer_3
        sigmoid_2 = ((self.z2*(1 - self.z2))).T
        
        sigmoid_x = sigmoid_2*self.z1.T
        
        self.deriv_2 = loss_layer_2.T*sigmoid_x
        self.bias_deriv_2 = loss_layer_2.T*sigmoid_2

        # #update weights between x and z1
        loss_layer_1 = np.sum(self.layer_2*loss_layer_2,axis=1, keepdims=True)
        
        sigmoid_1 = (self.z1*(1 - self.z1))
        sigmoid_x_1 = sigmoid_1*x        
        self.deriv_1 = sigmoid_x_1*loss_layer_1
        self.bias_deriv_1 = (loss_layer_1*sigmoid_1)

    def stochastic_grad_descent(self):
        for i in range(self.epoch):
            X, Y = shuffle(self.X, self.Y)
            for j in range(len(self.X)):
                y_pred = self.forwardPass(X[j])
                
                self.backwardsPass(Y[j], y_pred, X[j:j+1])
                self.update_weights(i)

    def prediction(self, x):
       #updating layer 1 
        z1 = self.sigmoid(np.sum(self.layer_1*x,axis= 1, keepdims=True) + self.bias_layer_1)
        #updating layer 2
        z2 = self.sigmoid(np.sum(self.layer_2.T*z1.T, axis= 0, keepdims=True).T + self.bias_layer_2).T
        #y output
        y_pred = np.sum(self.layer_3*z2, axis= 1) + self.bias_layer_3
        return np.sign(y_pred)
        


    def update_weights(self, t):
        r = self.r(self.r_0, self.d, t)

        self.layer_3 -= r*self.deriv_3
        self.bias_layer_3 -= r*self.bias_deriv_3

        self.layer_2 -= r*self.deriv_2
        self.bias_layer_2 -= r*self.bias_deriv_2

        self.layer_1 -= r*self.deriv_1
        self.bias_layer_1 -= r*self.bias_deriv_1

    def sigmoid_func(self, x):
        return 1/(1 + math.exp(-1*x))
    
    def testError(self, testData, labels):
        incorrectPred = 0
        
        for i in range(len(testData)):
            output = self.prediction(testData[i])
            if output != labels[i]:
                incorrectPred += 1
        
        return incorrectPred/len(testData)

def readFile(CSVfile):
    termList = []
    #Basic line reading. Need to sort by label
    with open(CSVfile, 'r') as file:
        for line in file:
            termList.append(np.array((line.strip().split(',')))) 

    termList = np.array(termList).astype(np.float)     
    result = np.hsplit(termList, np.array([4, 6]))
    trainingData  =result[0]
    labels = np.transpose(result[1])[0]
    labels[labels == 0] = -1
    return trainingData, labels

def lr_func(r, d, t):
    return r/(1 + (r/d)*t)

def generateWeights(width, features):
    #weights from x to z1
    w1 = np.random.normal(loc=.5, scale=.5,size=(width, features + 1))
    #weights from z1 to z
    w2 = np.random.normal(loc=.5, scale=.5,size=(width, width + 1))
    #weights from z2 to y
    w3 = np.random.normal(loc=.5, scale=.5,size=(1, width + 1))

    return w1, w2, w3

def generateWeightsZero(width, features):
    #weights from x to z1
    w1 = np.zeros([width, features + 1])
    #weights from z1 to z
    w2 = np.zeros([width, width + 1])
    #weights from z2 to y
    w3 = np.zeros([1, width + 1])

    return w1, w2, w3


train, labels = readFile("bank-note/train.csv")
test, testLabels = readFile("bank-note/test.csv")

widths = [5, 10, 25, 50, 100]
width = 10

w1, w2, w3 = generateWeightsZero(width, len(train[0]))

# w1 = np.array([[.1,.11,.21,.31, .41],
#                [.1,.12,.22,.32, .42],
#                [.1,.13,.23,.33, .43]])


# w2 = np.array([[1,.11, .12, .13],[1,.21, .22, .23],[1,.31,.32,.33]])
# nn = NeuralNetwork(train, labels, width, w1, w2,w3, 10, lr_func, .000005, .000001)
    
# nn.stochastic_grad_descent()
# print("Results for width of " + str(width) + ": " + str(nn.testError(test, testLabels)))
for width in widths:
    w1, w2, w3 = generateWeights(width, len(train[0]))
    print(w1)
    nn = NeuralNetwork(train, labels, width, w1, w2,w3, 100, lr_func, .00000005, .00000001)
        
    nn.stochastic_grad_descent()
    print("Results for width of " + str(width) + ": " + str(nn.testError(test, testLabels)))

    