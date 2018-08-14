'''
Use boradcast method to create an 4*4 array that has its 1st column full of 1's
2nd column full of 2's, 3rd column full of 3's etc
'''
import numpy as np

x= np.ones((4,4)) 
print(x)
y =np.arange(1,5)
print(y)
print(x*y)
