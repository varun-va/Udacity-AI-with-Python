'''
Hours Studied, Hours Slept (input)	Test Score (output)
2, 9	92
1, 5	86
3, 6	89
4, 8	?

2 inputs
3 hidden layers
1 output
'''
import numpy as np

#X = (hours of sleeping, hours of studying), y = score on test
X = np.array(([2,9],
              [1,5],
              [3,6]))
y = np.array(([92],
              [86],
              [89]))

#scale units, so that values are between 0 to 1

X = X/np.amax(X,axis = 0) # maximum of X array
y = y/100 #max test score is 100
print(X)
print(y)

class Neural_Network(object):
    def __init__(self):
        #parameters
        self.inputSize = 2
        self.outputSize = 1
        self.hiddenSize = 3
        
        #weights
        self.W1 = np.random.randn(self.inputSize,self.hiddenSize) #weight matrix from input to hidden layer (3x2)
        self.W2 = np.random.randn(self.hiddenSize,self.outputSize) # weight matrix from hidden layer to output (3x1)
    
    def sigmoid(self, s):
        return 1/(1+np.exp(-s))
    
    def forward(self,X):
        #forward propogation through the network
        self.z = np.dot(X,self.W1) #dot product of input X and first set of 3x2 input
        self.z2 = self.sigmoid(self.z) #activation function
        self.z3 = np.dot(self.z2,self.W2) #dot product  of hidden layer z2 and second set of weight 3x1
        o = self.sigmoid(self.z3) #final activation function
        return o

    
NN = Neural_Network()

#define output
o = NN.forward(X)

print("Predicted output: \n"+str(o))
print("Actual output: \n"+str(y))

'''
Predicted output: 
[[0.72884857]
 [0.69219904]
 [0.73106668]]
 
Actual output: 
[[0.92]
 [0.86]
 [0.89]]
'''
