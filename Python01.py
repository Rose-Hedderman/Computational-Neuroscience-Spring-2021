import random
import numpy as np

# Variables

""" x = 2
y = 5.434
s = 'this is a string'
x = 5.555
a = int(4.432)
data_1 = 5.5
print(a) """

# Lists/Arrays
# collection of same type of variables saved together
""" my_list= []
my_list.append(3)
my_list.append(6)
my_list.append(10)
print(my_list)
my_list.pop()
print(my_list) """

# Loops
# have to import random, initally a dark green which implies you haven't used it yet

""" my_list = []

for i in range(0,10):
    my_list.append(random.random())

print(my_list) """

# numpy
""" npList = np.zeros(10)
npList2 = np.ones(20)

npList[5] = 3.3
print(npList) """

# sort
npList = np.zeros(10)
for i in range(0,10):
    npList[i] = random.random()
print(npList.sort())

