# program to illustrate use of classes

import numpy as np
sweepLength = 1000
""" 
Vm = np.zeros(sweepLength)
Thresh = np.zeros(sweepLength)
gE = np.zeros(sweepLength)
gI = np.zeros(sweepLength)
Ena = 6.0
Ek = -75.0
Eleak = -70.0
gLeak = 0.1
capacitance = 30

for t in range(1,sweepLength):  # simulate the neuron for one sweep
    dVm = (gLeak*(Eleak-Vm[t-1]))/capacitance # only a leak current
    Vm[t] = Vm[t-1] + dVm   # driving force
    print(t, Vm[t])
 """
""" 
class neuron():
    def __init__(self, sweep):
        self.Vm = np.zeros(sweep)
        self.Thresh = np.zeros(sweep)
        self.gE = np.zeros(sweep)
        self.gI = np.zeros(sweep)
        self.Ena = 6.0
        self.Ek = -75.0
        self.Eleak = -70.0
        self.gLeak = 0.1
        self.capacitance = 30

gr = neuron(sweepLength)

for t in range(1,sweepLength):  # simulate the neuron for one sweep
    dVm = (gr.gLeak*(gr.Eleak-gr.Vm[t-1]))/gr.capacitance # only a leak current
    gr.Vm[t] = gr.Vm[t-1] + dVm   # driving force
    print(t, gr.Vm[t])
 """

 # classes can contain functions
""" 
class neuron():
    def __init__(self, sweep):
        self.sweepLength = 5000
        self.Vm = np.zeros(sweep)
        self.Thresh = np.zeros(sweep)
        self.gE = np.zeros(sweep)
        self.gI = np.zeros(sweep)
        self.Ena = 6.0
        self.Ek = -75.0
        self.Eleak = -70.0
        self.gLeak = 0.1
        self.capacitance = 30
    
    def doSweep(self):
        for t in range(1,sweepLength):  # simulate the neuron for one sweep
            dVm = (self.gLeak*(self.Eleak-self.Vm[t-1]))/self.capacitance # only a leak current
            self.Vm[t] = self.Vm[t-1] + dVm   # driving force
            print(t, self.Vm[t])

gr = neuron(sweepLength)
gr.doSweep()
 """

# final example

class neuron():
    def __init__(self, sweep):
        self.sweepLength = sweep
        self.Vm = np.zeros(sweep)
        self.Thresh = np.zeros(sweep)
        self.gE = np.zeros(sweep)
        self.gI = np.zeros(sweep)
        self.Ena = 6.0
        self.Ek = -75.0
        self.Eleak = -70.0
        self.gLeak = 0.1
        self.capacitance = 30
    
    def doSweep(self):
        for t in range(1,sweepLength):  # simulate the neuron for one sweep
            dVm = (self.gLeak*(self.Eleak-self.Vm[t-1]))/self.capacitance # only a leak current
            self.Vm[t] = self.Vm[t-1] + dVm   # driving force
            print(t, self.Vm[t])

gr = []
for i in range(0,10):
    gr.append(neuron(sweepLength))
for x in gr:
    x.doSweep()

