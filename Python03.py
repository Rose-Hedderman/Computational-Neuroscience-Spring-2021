# Program to illustrate use of function
import random as ran

def happyComment():
    print()
    x = ran.random()        # print an encouraging comment
    if x > 0.75:
        print('Everything will be okay')
    elif x > 0.5:
        print('Keep similing')
    elif x > 0.25:
        print("Hang in there")
    else:
        print('Have a great day')
    print()

def sumSquares(n):
    # scope is where in the program a variable can be used
    ss = 0
    for x in n:
        ss += x*x
    return ss

def smallLarge(n):
    sm = min(n)
    lg = max(n)
    return sm, lg

## program beings here
happyComment()

numbers = [4, 6, 7, 4, 7, 11, 45]
ss = sumSquares(numbers)
print(ss)
[smallest, largest] = smallLarge(numbers)
happyComment()
print(smallest, largest)
happyComment()
