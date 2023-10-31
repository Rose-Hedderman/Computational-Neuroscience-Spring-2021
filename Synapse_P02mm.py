import numpy as np
import math 
import random

class Synapse():
    def __init__(self):
        self.duration = 1000
        # numpy lists
        self.Vm = np.zeros(self.duration)
        self.gExcite = np.zeros(self.duration)
        self.gInhibit = np.zeros(self.duration) # not used right now
        self.CalciumEx = np.zeros(self.duration)
        self.ReleaseP_Ex = np.zeros(self.duration)
        self.Docked = np.zeros(self.duration)
        self.NT = np.zeros(self.duration)
        self.Bound = np.zeros(self.duration)

        # parameters
        self.gLeak = .15
        self.ELeak = -70      # all voltages are in mV
        self.Capacitance = .5    # units? uFarads
        # excitatory synapse 
        self.EExcite = -10
        self.ExciteMaxg = .5
        self.ExciteTau = 5
        self.ExciteDecay = math.exp(-1/self.ExciteTau)
        # inhibitory synapse
        self.EInhibit = -80
        self.InhibitStrength = .03
        self.InhibitTau = 20
        self.InhibitDecay = math.exp(-1/self.InhibitTau)
        # Calcium parameters
        self.CaTauEx = 40
        self.CaDecayEx = math.exp(-1/self.CaTauEx)
        self.CaIncrementEx = .2
        # vesicles and receptor parameters
        self.maxDocked = 500
        self.Vesicles = np.ones(self.maxDocked)
        self.VesicleReplenishTau = 500
        self.VesicleDecay = 1 - math.exp(-1/self.VesicleReplenishTau)
        # Neurotransmitter (NT)
        self.NTperVesicle = 100
        self.numReceptors = 1000
        self.NTtau = 2
        self.NTdecay = math.exp(-1/self.NTtau)

        # set initial values
        self.Vm[0] = self.ELeak        # this will be useful later

    def DoTimeStep(self,t,Espike,Ispike,index,offset,exponent): # t is the time step, Espike and Ispike= 1 or 0
        
        if Espike ==1: # update excitatory synapse conductance
            self.CalciumEx[t] = self.CalciumEx[t-1] + ((1-self.CalciumEx[t-1])*self.CaIncrementEx)
        else: #let excitatory conductance decay
            self.CalciumEx[t] = self.CalciumEx[t-1] * self.CaDecayEx

        self.ReleaseP_Ex[t] = self.DoRelease(self.CalciumEx[t],index, offset, exponent)
        # self.gExcite[t] = self.release[t]*.2  #update gExcite by release   
        
        releaseTotal = 0
        self.Docked[t] = 0
        #use release probability to determine which vesicles are released
        for v in range(0,self.maxDocked):
            if random.random() < self.ReleaseP_Ex[t] * self.Vesicles[v] * 0.0125: 
                releaseTotal += 1
                self.Vesicles[v] = 0
            self.Docked[t] += self.Vesicles[v]    
            if random.random()<self.VesicleDecay: self.Vesicles[v] = 1
        self.gExcite[t] = self.gExcite[t-1]+(releaseTotal * (6.0/self.maxDocked))
        self.gExcite[t] *= self.ExciteDecay

        # calculate the currents
        Ileak = self.gLeak*(self.ELeak-self.Vm[t-1]) # calculate leak current
        IExcite = self.gExcite[t-1]*(self.EExcite-self.Vm[t-1])
        #IInhibit = self.gInhibit[t-1]*(self.EInhibit-self.Vm[t-1])
        Im = Ileak + IExcite #+ IInhibit  # sum of currents = total membrane current
        
        self.Vm[t] = self.Vm[t-1] + (Im/self.Capacitance) # calculate change in Vm
        
        # write last values to first in case it's running continuously
        if t == self.duration -1:
            self.gExcite[0] = self.gExcite[self.duration-1]
            self.gInhibit[0] = self.gInhibit[self.duration-1]
            self.Vm[0] = self.Vm[self.duration-1]
        return self.Vm[t]  # return that value

    def DoSweep(self,interval,index,offset,exponent):  # Use this to calculate the whole sweep at once, then draw all at once.  it's faster this way
        for bin in range(1,self.duration):
            Es = 0
            Is = 0
            if (bin > 180) and (bin < 550) and (bin%50 ==0): # or (bin == 920):  
            #if bin == 200 or bin ==200+interval: 
                Es = 1
            self.Vm[bin] = self.DoTimeStep(bin,Es,Is,index,offset,exponent)
        return self.Vm 

    def DoRelease(self,calcium,index,arg1,arg2):
        if index == 1:  # sigmoidal: here arg1 is offset and arg2 is exponent
            offset = arg1       # 4
            exponent = arg2     # 6
            x = -5+(calcium*10)+offset
            z = 1/(1 + np.exp(-x))
            release = z**exponent 
        elif index == 2: # linear with threshold, arg1 is threshold, arg2 is where max release is reached
            thresh = arg1       # .15
            max = arg2          # .35
            if calcium < thresh:
                release = 0
            elif calcium > max:
                release = 1
            else:  
                slope = 1/(max - thresh)
                release = slope*(calcium-thresh)
            if release > 1: release = 1
        elif index == 3:    #sigmoidal using algebraic equation 
            x = -7+(calcium*10)-arg1
            z =( (x+5) / math.sqrt(1 + ((x+5)**2)) ) +1
            release = z*0.5
            release = release**arg2
        elif index ==4:
            release = calcium * arg1
        return release
    
    def showRelease(self,index, arg1, arg2):
        release = np.zeros(1000)
        for i in range(0,1000):
            c = i *.001
            release[i] = self.DoRelease(c, index, arg1, arg2)
        return release
                
