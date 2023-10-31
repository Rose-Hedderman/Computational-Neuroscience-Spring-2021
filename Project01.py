import numpy as np
import math

class Project01Neuron():
    def __init__(self):
        self.duration = 2500    # 2.5 seconds
        self.timestep = 1      # in milliseconds

        self.Vm = np.zeros(self.duration)
        self.Thresh = np.zeros(self.duration)
        # make a arrays because they change over time

        # calcium concentration (0(min) to 1(max))
        # potassium conductance depends on calcium concentration
            # yellow in leaky integrate and fire
            # proportional to calc conc (0.01?) also from 0 to 1
        # when it spikes THEN calcium increases, all other times, exp decreasing
        self.CaConc = 0.5
        self.gK = 0.5

        # parameters
        self.gLeak = 0.01   # relatively small leak conductance
        self.ELeak = -48    # all voltages are in mV
        self.capacitance = 1 


        # parameters about Threshold
        self.ThreshBase = -50
        self.ThreshMax = 10 # in mV
        self.ThreshTau = 20 # in milliseconds
        self.ThreshDecay = 1 - (math.exp(-1/self.ThreshTau))    # complicated/ known equation

        # set inital values
        self.Vm[0] = -75
        self.Thresh[0] = self.ThreshBase
        
        
    def DoTimeStep(self, t):        
        Ileak = self.gLeak*(self.ELeak-self.Vm[t-1]) # calculate leak current
        self.Vm[t] = self.Vm[t-1] + (Ileak/self.capacitance) # calculate charge in Vm

        # at every time step, you want threshold to be decaying back to base
        self.Thresh[t] = self.Thresh[t-1] + (self.ThreshDecay * (self.ThreshBase - self.Thresh[t-1]))

        # decay for calcium conc..etc taks 5
            # can be same as thresh decay but change calcium tau

        if self.Vm[t] > self.Thresh[t]: # if the membrane potential is greater than the threshold
            spike = 1
            self.Thresh[t] = self.ThreshMax
            # increase calcium for task 5
        else:
            spike = 0

        return self.Vm[t], self.Thresh[t], spike    # return those value