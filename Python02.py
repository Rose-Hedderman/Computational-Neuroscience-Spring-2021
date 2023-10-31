import random as r
import numpy as np

numData = 10 # this is the number of data points
threshold = 0.6 # this is the cutoff value for my while loop

data = np.zeros(numData)
x = 0.0
counter = 0
RB = 'really big'
KB = 'kinda big'
w = 'whatever'
S = 'small'

for i in range(0,numData): # fills data with random numbers
    data[i] = r.random()

# print(numData,data)

""" 
while x < threshold:
x = data[counter]
counter += 1 
"""

for i in range(numData):
    x = data[i]
    if x > 0.8:
        print(RB)
    elif x > threshold:
        print(KB)
    elif x > 0.3:
        print(w)
    else:
        print(S)

print(x)