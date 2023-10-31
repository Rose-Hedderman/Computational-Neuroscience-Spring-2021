import numpy as np
import math

class HH1952():
    def __init__(self):
        self.duration = 5000
        self.dt = .008
        self.EK = -80.0
        self.ENa = 60.0
        self.Vm = np.zeros(self.duration)
        self.IK = np.zeros(self.duration)
        self.Ileak = np.zeros(self.duration)
        self.INa = np.zeros(self.duration)
        self.Imemb = np.zeros(self.duration)

        self.gNa = np.zeros(self.duration)
        self.gK = np.zeros(self.duration)
        
        self.m = np.zeros(self.duration)
        self.mAlpha = np.zeros(self.duration)
        self.mBeta = np.zeros(self.duration)
        self.m8 = np.zeros(self.duration)
        
        self.h = np.zeros(self.duration)
        self.h8 = np.zeros(self.duration)
        self.hAlpha = np.zeros(self.duration)
        self.hBeta = np.zeros(self.duration)
        
        self.n = np.zeros(self.duration)
        self.nAlpha = np.zeros(self.duration)
        self.nBeta = np.zeros(self.duration)
        self.n8 = np.zeros(self.duration)

        self.gNamax = 128.0
        self.gKmax = 36.0
        self.gLeak = .3

        self.Istim = np.zeros(self.duration)
        self.initialize(1)
        self.Vm[0] = -75.5
        self.gKOn = 1
        self.gNaOn = 1
        self.doStim()
    def initialize(self,numPoints):
        for i in range(0,numPoints):
            #self.Vm[i]= -75.5
            self.gNa[i] = 0.0
            self.gK[i] = 0.0
            self.h[i] = .94

            self.hAlpha[i] = .1558
            self.hBeta[i] = .01
            
            self.IK[i] = 0.0
            self.Ileak[i] = 0.0
            self.Imemb[i] = 0.0
            self.INa[i] = 0.0
            self.m[i] = .0071
            self.mAlpha[i] = .0691
            self.mBeta[i] = 9.7297
            self.n[i] = .1161
            self.nAlpha[i] = .0209
            self.nBeta[i] = .1588
            self.Istim[i] = 0.0
    def doStim(self):
        for t in range(1000,1500):
            self.Istim[t] = 10
    def do_K(self,V,t):  #Voltage-gated K
        self.nAlpha[t] = .01*(V+10)/(math.exp((V+10)/10)-1)
        self.nBeta[t] = .125*math.exp(V/80)
        self.n8[t] = self.nAlpha[t]/(self.nAlpha[t]+self.nBeta[t])
        self.n[t] = self.n[t-1] + ((self.nAlpha[t]*(1-self.n[t-1]))-(self.nBeta[t]*self.n[t-1]))*self.dt
        #return math.pow(self.nAlpha[t]/(self.nAlpha[t]+self.nBeta[t]),4), self.nAlpha[t], self.nBeta[t]
    def do_Na(self,V,t): #Voltage-gated Na activation
        self.mAlpha[t] = .1*(V+25.0)/(math.exp((V+25.0)/10.0)-1)
        self.mBeta[t] = 4.0*math.exp(V/18)
        self.m8[t] = self.mAlpha[t]/(self.mAlpha[t]+self.mBeta[t])
        self.m[t] = self.m[t-1] + ((self.mAlpha[t]*(1-self.m[t-1]))-(self.mBeta[t]*self.m[t-1]))*self.dt
        #return math.pow(self.mAlpha[t]/(self.mAlpha[t]+self.mBeta[t]),3), self.mAlpha[t], self.mBeta[t]
    def do_NaInactivation(self,V,t,h):
        self.hAlpha[t] = .07*math.exp(V/20.0)
        self.hBeta[t] = 1/((math.exp((V+30.0)/10)+1))
        self.h8[t]= self.hAlpha[t]/(self.hAlpha[t]+self.hBeta[t])
        self.h[t] = self.h[t-1] + ((self.hAlpha[t]*(1-self.h[t-1]))-(self.hBeta[t]*self.h[t-1]))*self.dt
        # self.h[t] = 1.0-((1-self.h[t])*h)
        # if self.h[t] < 0: self.h[t]=0.0
        #return self.hAlpha[t]/(self.hAlpha[t]+self.hBeta[t]), self.hAlpha[t], self.hBeta[t]
    def doCurrents(self,V,t,Na,K): #Conductances and membrane current
        self.gK[t] = self.gKOn*(1-(math.pow(self.n[t],4))*self.gKmax)
        self.gNa[t] = self.gNaOn*(1-(((math.pow(self.m[t],3))*self.h[t]*self.gNamax))+.01) 
        self.IK[t] = (self.EK-V)*(self.gK[t])*K
        self.INa[t] = (self.ENa-V)*(self.gNa[t])*Na
        self.Ileak[t] = self.gLeak*(self.EK-V)
        self.Imemb[t] = self.IK[t]+self.INa[t]+self.Ileak[t]+self.Istim[t]
    def runSim(self,Na,K,h):
        self.doStim()
        for timebin in range(1,self.duration):
            self.do_K(self.Vm[timebin-1],timebin)
            self.do_Na(self.Vm[timebin-1],timebin)
            self.do_NaInactivation(self.Vm[timebin-1],timebin,h)
            self.doCurrents(self.Vm[timebin-1],timebin,Na,K)
            self.Vm[timebin] = self.Vm[timebin-1]+(self.Imemb[timebin]*self.dt)
        return self.Vm, self.INa, self.IK, self.Imemb, self.gNa, self.gK
    
class HHneuron():
    def __init__(self):
        self.duration = 5000
        self.dt =  .008
        self.EK =  -80
        self.ENa =  60
        self.nAlpha1 =  .01      # n params
        self.nAlpha2 =  -62.0
        self.nAlpha3 =  10.0
        self.nAlpha4 =  10.0
        self.nBeta1 =  .13
        self.nBeta2 =  -62.0
        self.nBeta3 =  80.0
        self.mAlpha1 =  .1     # m params
        self.mAlpha2 =  -62.0
        self.mAlpha3 =  25.0
        self.mAlpha4 =  10.0
        self.mBeta1 =  4.0
        self.mBeta2 =  -62.0
        self.mBeta3 =  18.0      # h params
        self.hAlpha1 =  .07
        self.hAlpha2 =  62.0
        self.hAlpha3 =  -20.0
        self.hBeta1 =  -32.0
        self.hBeta2 =  10.0      # conductances
        self.gNamax =  128.0
        self.gKmax =  36.0
        self.gLeak =  .3

        self.gNa = np.zeros(self.duration)
        self.gK = np.zeros(self.duration)
        self.Vm = np.zeros(self.duration)
        self.h = np.zeros(self.duration)
        self.hAlpha = np.zeros(self.duration)
        self.hBeta = np.zeros(self.duration)
        self.IK = np.zeros(self.duration)
        self.Ileak = np.zeros(self.duration)
        self.Imemb = np.zeros(self.duration)
        self.INa = np.zeros(self.duration)
        self.m = np.zeros(self.duration)
        self.mAlpha = np.zeros(self.duration)
        self.mBeta = np.zeros(self.duration)
        self.n = np.zeros(self.duration)
        self.nAlpha = np.zeros(self.duration)
        self.nBeta = np.zeros(self.duration)

        self.Istim = np.zeros(self.duration)
        self.initialize(1)
        self.Vm[0] = -75.5
        self.gKOn = 1
        self.gNaOn = 1
        self.doStim()
    def initialize(self,numPoints):
        for i in range(0,numPoints):
            #self.Vm[i]= -75.5
            self.gNa[i] = 0.0
            self.gK[i] = 0.0
            self.h[i] = .94

            self.hAlpha[i] = .1558
            self.hBeta[i] = .01
            
            self.IK[i] = 0.0
            self.Ileak[i] = 0.0
            self.Imemb[i] = 0.0
            self.INa[i] = 0.0
            self.m[i] = .0071
            self.mAlpha[i] = .0691
            self.mBeta[i] = 9.7297
            self.n[i] = .1161
            self.nAlpha[i] = .0209
            self.nBeta[i] = .1588
            self.Istim[i] = 0.0
    def doStim(self):
        for t in range(1000,1500):
            self.Istim[t] = 10
    def do_K(self,V,t):  #Voltage-gated K
        self.nAlpha[t] = (self.nAlpha1*(self.nAlpha2 + self.nAlpha3-V))/(-1+ math.exp(((-1*V) + self.nAlpha2 + self.nAlpha3)/self.nAlpha4))
        self.nBeta[t] = self.nBeta1 * math.exp((self.nBeta2-V)/self.nBeta3)
        self.n[t] = self.n[t-1] + ((self.nAlpha[t]*(1-self.n[t-1]))-(self.nBeta[t]*self.n[t-1]))*self.dt
        return self.nAlpha[t], self.nBeta[t]
    def do_Na(self,V,t): #Voltage-gated Na activation
        self.mAlpha[t] = (self.mAlpha1*(self.mAlpha2+self.mAlpha3-V))/(-1+math.exp((self.mAlpha2+self.mAlpha3-V)/self.mAlpha4))
        self.mBeta[t] = self.mBeta1*math.exp((self.mBeta2-V)/self.mBeta3)
        self.m[t] = self.m[t-1] + ((self.mAlpha[t]*(1-self.m[t-1]))-(self.mBeta[t]*self.m[t-1]))*self.dt
        return self.mAlpha[t], self.mBeta[t]
    def do_NaInactivation(self,V,t,h):
        self.hAlpha[t] = self.hAlpha1*math.exp((self.hAlpha2+V)/self.hAlpha3)
        self.hBeta[t] = 1/(1+math.exp((self.hBeta1-V)/self.hBeta2))
        self.h[t] = self.h[t-1] + ((self.hAlpha[t]*(1-self.h[t-1]))-(self.hBeta[t]*self.h[t-1]))*self.dt
        self.h[t] = 1.0-((1-self.h[t])*h)
        if self.h[t] < 0: self.h[t]=0.0
        return self.hAlpha[t], self.hBeta[t]
    def doCurrents(self,V,t,Na,K): #Conductances and membrane current
        self.gK[t] = self.gKOn*((math.pow(self.n[t],4))*self.gKmax)
        self.gNa[t] = self.gNaOn*(((math.pow(self.m[t],3))*self.h[t]*self.gNamax))+.01 
        self.IK[t] = (self.EK-V)*(self.gK[t])*K
        self.INa[t] = (self.ENa-V)*(self.gNa[t])*Na
        self.Ileak[t] = self.gLeak*(self.EK-V)
        self.Imemb[t] = self.IK[t]+self.INa[t]+self.Ileak[t]+self.Istim[t]
    def runSim(self,Na,K,h):
        self.doStim()
        for timebin in range(1,self.duration):
            self.do_K(self.Vm[timebin-1],timebin)
            self.do_Na(self.Vm[timebin-1],timebin)
            self.do_NaInactivation(self.Vm[timebin-1],timebin,h)
            self.doCurrents(self.Vm[timebin-1],timebin,Na,K)
            self.Vm[timebin] = self.Vm[timebin-1]+(self.Imemb[timebin]*self.dt)
        return self.Vm, self.INa, self.IK, self.Imemb, self.gNa, self.gK

class CorticalNeuron():
    def __init__(self):
        self.duration = 5000
        self.dt = .0001
        self.EK = -77.0
        self.ENa = 55.0
        self.Eleak = -65

        self.Vm = np.zeros(self.duration)
        self.IK = np.zeros(self.duration)
        self.Ileak = np.zeros(self.duration)
        self.INa = np.zeros(self.duration)
        self.Imemb = np.zeros(self.duration)

        self.gNa = np.zeros(self.duration)
        self.gK = np.zeros(self.duration)
        
        self.m = np.zeros(self.duration)
        self.mAlpha = np.zeros(self.duration)
        self.mBeta = np.zeros(self.duration)
        self.m8 = np.zeros(self.duration)
        
        self.h = np.zeros(self.duration)
        self.h8 = np.zeros(self.duration)
        self.hAlpha = np.zeros(self.duration)
        self.hBeta = np.zeros(self.duration)
        
        self.n = np.zeros(self.duration)
        self.nAlpha = np.zeros(self.duration)
        self.nBeta = np.zeros(self.duration)
        self.n8 = np.zeros(self.duration)

        self.gNamax = 120.0
        self.gKmax = 35.0
        self.gLeak = .3

        self.Istim = np.zeros(self.duration)
        self.initialize(1)
        self.Vm[0] = -77.0
        self.gKOn = 1
        self.gNaOn = 1
        self.doStim()
    def initialize(self,numPoints):
        for i in range(0,numPoints):
            #self.Vm[i]= -75.5
            self.gNa[i] = 0.0
            self.gK[i] = 0.0
            self.h[i] = .94

            self.hAlpha[i] = .1558
            self.hBeta[i] = .01
            
            self.IK[i] = 0.0
            self.Ileak[i] = 0.0
            self.Imemb[i] = 0.0
            self.INa[i] = 0.0
            self.m[i] = .0071
            self.mAlpha[i] = 0
            self.mBeta[i] = 1
            self.n[i] = .1161
            self.nAlpha[i] = .0209
            self.nBeta[i] = .1588
            self.Istim[i] = 0.0
    def doStim(self):
        for t in range(1000,3000):
            self.Istim[t] = 10
    def do_K(self,V,t):  #Voltage-gated K
        self.nAlpha[t] =  .02*(V-25)/(1-math.exp(-1*(V-25)/9))    
        self.nBeta[t] = (-.002*(V-25))/(1-math.exp((V-25)/9))
        self.n8[t] = self.nAlpha[t]/(self.nAlpha[t]+self.nBeta[t])
        self.n[t] = self.n[t-1] + ((self.nAlpha[t]*(1-self.n[t-1]))-(self.nBeta[t]*self.n[t-1]))*self.dt
        return math.pow(self.nAlpha[t]/(self.nAlpha[t]+self.nBeta[t]),4), self.nAlpha[t], self.nBeta[t]
    def do_Na(self,V,t): #Voltage-gated Na activation
        self.mAlpha[t] = .182*(V+35.0) / (1-(math.exp(-1*(V+35)/9.0)))
        self.mBeta[t] = -.124*(V+35) / (1-math.exp((V+35)/9))
        self.m8[t] = self.mAlpha[t]/(self.mAlpha[t]+self.mBeta[t])
        self.m[t] = self.m[t-1] + ((self.mAlpha[t]*(1-self.m[t-1]))-(self.mBeta[t]*self.m[t-1]))*self.dt
        return math.pow(self.mAlpha[t]/(self.mAlpha[t]+self.mBeta[t]),3), self.mAlpha[t], self.mBeta[t]
    def do_NaInactivation(self,V,t,h):
        self.hAlpha[t] = .25*math.exp(-1*(90.0+V)/12)
        self.hBeta[t] =  .25*(math.exp((V+62)/6))/math.exp((V+90)/12)
        self.h8[t]= self.hAlpha[t]/(self.hAlpha[t]+self.hBeta[t])
        self.h[t] = self.h[t-1] + ((self.hAlpha[t]*(1-self.h[t-1]))-(self.hBeta[t]*self.h[t-1]))*self.dt
        # self.h[t] = 1.0-((1-self.h[t])*h)
        # if self.h[t] < 0: self.h[t]=0.0
        return self.hAlpha[t]/(self.hAlpha[t]+self.hBeta[t]), self.hAlpha[t], self.hBeta[t]
    def doCurrents(self,V,t,Na,K): #Conductances and membrane current
        self.gK[t] = self.gKOn*(1-(math.pow(self.n[t],4))*self.gKmax)
        self.gNa[t] = self.gNaOn*(1-(((math.pow(self.m[t],3))*self.h[t]*self.gNamax))+.01) 
        self.IK[t] = (self.EK-V)*(self.gK[t])*K
        #self.IK[t] = 0
        self.INa[t] = (self.ENa-V)*(self.gNa[t])*Na
        #self.INa[t] = 0
        self.Ileak[t] = self.gLeak*(self.Eleak-V)
        self.Imemb[t] = self.IK[t]+self.INa[t]+self.Ileak[t]+self.Istim[t]
    def runSim(self,Na,K,h):
        self.doStim()
        for timebin in range(1,self.duration):
            self.do_K(self.Vm[timebin-1],timebin)
            self.do_Na(self.Vm[timebin-1],timebin)
            self.do_NaInactivation(self.Vm[timebin-1],timebin,h)
            self.doCurrents(self.Vm[timebin-1],timebin,Na,K)
            self.Vm[timebin] = self.Vm[timebin-1]+(self.Imemb[timebin]*self.dt)
            #print(self.Vm[timebin])
        return self.Vm

class VoltageClamp(HHneuron):
    def __init__(self):
        super().__init__()
        
    def doCommandVoltage(self,h,s):
        for t in range(0,self.duration):
            self.Vm[t] = h
        for t in range(1000,4000):
            self.Vm[t] = s

    def doVoltageStep(self,Na,K,h,hold,step):
        self.doCommandVoltage(hold,step)
        for t in range(0,self.duration):
            V = self.Vm[t]
            self.do_Na(V,t)
            self.do_NaInactivation(V,t,h)
            self.do_K(V,t)
            self.doCurrents(V,t,Na,K)
        return self.Imemb,self.Vm

class IzhikevichNeuron():
    def __init__(self):
        self.FirstTime = 1
        self.duration = 1000          # how long to run the sim
        self.input_onset = 300           # onset time of input
        self.input_amp = 6               # input amplitude
        self.timeStep = 0.5            # time step size
        self.numTimeSteps = int((1//self.timeStep)*self.duration)
        self.time=np.arange(0,self.duration,self.timeStep)            # array that holds the time in ms for each step
        self.Vm=-65.0*np.ones(self.numTimeSteps)  # initial value of the membrane potential variable IZVm
        self.u=0.0*np.ones(self.numTimeSteps)     # initial value of the membrane recovery variable u
        self.I=np.zeros(self.numTimeSteps)            # I = input current

    def StimCurrent(self):
        for k in range (0,self.numTimeSteps):
            if self.time[k] > self.input_onset:
                self.I[k]=self.input_amp     # stimulation current is input_amp at these times
    def runSim(self,a,b,c,d):
        self.StimCurrent()
        if self.FirstTime == 1: 
            self.Vm[0] = -65.0
            self.u[0]=b*self.Vm[0]   
            self.FirstTime = 0
        for k in range (0,self.numTimeSteps-1):
            uM = self.u[k]
            vM = self.Vm[k]
            self.Vm[k+1] = vM + self.timeStep *(0.04*vM*vM+5*vM+140-uM+self.I[k])
            self.u[k+1] = uM + self.timeStep *(a*(b*vM-uM))  
            if self.Vm[k+1]>30:
                self.Vm[k+1]=c
                self.u[k+1]=self.u[k+1]+d
            self.Vm[0]=self.Vm[self.numTimeSteps-1]
            self.u[0]=self.u[self.numTimeSteps-1]
        return self.Vm

class IOneuron():
    def __init__(self):
        self.FirstTime = 1
        self.duration = 100000
        self.timestep = .01  # this is a guess  10 usec
        self.ENa = 55.0
        self.EK = -75.0
        self.ECa = 120.0
        self.Eleak = -50.0
        self.Eh = -43.0
        self.Cm = 1.0

        ## MEMBRANE POTENTIAL and membrane current
        self.VmSoma = np.zeros(self.duration)
        self.VmDend = np.zeros(self.duration)
        self.Im_soma = np.zeros(self.duration)
        self.Im_dend = np.zeros(self.duration)
        self.VmSoma[0]=self.EK
        self.VmDend[0]=self.EK
       
        ###### SOMATIC currents
        ## sodium
        self.Na_gMax = 70.0
        self.Na_I = np.zeros(self.duration)
        self.Na_g = np.zeros(self.duration)
        self.Na_m = np.zeros(self.duration)
        self.Na_h = np.ones(self.duration)
        self.Na_hTau = np.zeros(self.duration)
        
        # Delayed recifier (Kd)
        self.Kd_gMax = 18.0
        self.Kd_I = np.zeros(self.duration)
        self.Kd_g = np.zeros(self.duration)
        self.Kd_n = np.zeros(self.duration)
        self.Kd_nTau = np.zeros(self.duration)

        ## Calcium low threshold
        self.ICaLow = np.zeros(self.duration)
        self.k = np.zeros(self.duration)
        self.tauk = np.zeros(self.duration)
        self.low = np.zeros(self.duration)
        self.taulow = np.zeros(self.duration)
        self.gCaLow = .2
       
        ## h (hyperpolarizatoin current)
        self.gh = 1.5
        self.Ih = np.zeros(self.duration)
        self.q = np.zeros(self.duration)
        self.tauq = np.zeros(self.duration)
        self.l = np.zeros(self.duration)
        self.taul = np.zeros(self.duration)
        
        ## somatic leak
        self.gleakS = .015
        self.IleakS = np.zeros(self.duration)
        
        
        ## DENDRITIC currents
        # calcium high threshold
        self.CaHigh_gMax = 1.0
        self.CaHigh_I = np.zeros(self.duration)
        self.CaHigh_r = np.zeros(self.duration)
        self.CaHigh_Taur = np.zeros(self.duration)
        self.CaHigh_g = np.zeros(self.duration)
        
        # Calcium activated potassium
        self.KCa_gMax = 40.0
        self.KCa_g = np.zeros(self.duration)
        self.KCa_I = np.zeros(self.duration)
        self.KCa_s = np.zeros(self.duration)
        #self.KCa_Taus = np.zeros(self.duration)
        self.Calcium = np.zeros(self.duration)
        
        # leak
        self.D_gleak = .015
        self.D_Ileak = np.zeros(self.duration)
        
        ## COUPLING currents
        # soma dendrite current
        self.Isd = np.zeros(self.duration)
        self.Ids = np.zeros(self.duration)

        # cell cell coupling
        self.ICouple = np.zeros(self.duration)
        # connectivity parameters
        self.p = 0.25
        self.gint = .13
        
    ### Dendrite functions
    def do_CaHigh(self,V,t):
        # flawed parameters from Schweighofer Doya Kawato 1999
        # r_alpha = 1.6/(1+math.exp(-1*(V-5.0)/14.0))
        # r_beta = (.02*(V+8.51))/(1-math.exp((V+8.51)/5.0))
        # r_beta = 9.0*math.exp(-1*(V+66)/20) # this is just beta from Na, there is an error for this in paper
        # self.CaHigh_Taur[t] = 1/(r_alpha+r_beta)
        # r8 = r_alpha/(r_alpha+r_beta)
        # from Manor Rinzel Segev and Yarom, 1997
        h8 = 1/(1+math.exp((V+85.5)/8.6))
        m8 = 1/(1+math.exp((-61.1-V)/4.2))
        tau = ((30/(1+math.exp((V+84)/7.3)))*math.exp((V+160)/30))+40
        tau = tau/1000.0
        #
        self.CaHigh_r[t]= self.CaHigh_r[t-1]+((self.timestep*(m8-self.CaHigh_r[t-1])/tau))
        self.CaHigh_g[t] = self.CaHigh_gMax*math.pow(self.CaHigh_r[t],3)*h8
        self.CaHigh_I[t] = self.CaHigh_g[t]*(self.ECa-V)
        return m8, h8, math.pow(m8,3)*h8*50
    def doCalcium(self,t):
        self.Calcium[t] = self.Calcium[t-1] + self.timestep*((3.0*self.CaHigh_I[t])-(.075*self.Calcium[t-1]))
    def do_KCa(self,V,t):
        s_alpha = self.Calcium[t]*.000000024485
        if s_alpha < 0: s_alpha = 0
        s_beta = .015
        s8 = s_alpha/(s_alpha+s_beta)
        s_tau = 1/(s_alpha+s_beta)
        #print (t,s_tau)
        self.KCa_s[t] = self.KCa_s[t-1]+(self.timestep*(s8-self.KCa_s[t-1]/s_tau))
        self.KCa_g[t] = self.KCa_gMax*self.KCa_s[t]
        self.KCa_I[t] = self.KCa_g[t]*(self.EK-V)
        #if t%100==0: print(self.Calcium[t],self.KCa_I[t],self.CaHigh_I[t])
    ### Soma functions
    def do_Na(self,V,t):
        m_alpha = (.1*(V + 41))/(1 - math.exp(-1*(V+41)/10))
        m_beta = 9.0*math.exp(-1*(V+66)/20)
        self.Na_m[t] = m_alpha/(m_alpha+m_beta) # these models assume m is instantaneous, so there is no m_tau
        #h
        h_alpha = 5.0*math.exp(-1*(V+60.0)/15.0)
        h_beta = (V+50)/(1-math.exp(-1*(V+50)/10.0))
        h8 = h_alpha/(h_alpha+h_beta)
        self.Na_hTau[t] = 170.0/(h_alpha+h_beta)
        self.Na_h[t]= self.Na_h[t-1] + (self.timestep*((h8-self.Na_h[t-1])/self.Na_hTau[t]))
        self.Na_g[t] = self.Na_gMax*math.pow(self.Na_m[t],3)*self.Na_h[t]
        self.Na_I[t] = self.Na_g[t]*(self.ENa - V)
        return math.pow(m_alpha/(m_alpha+m_beta),3), m_alpha, m_beta
    def do_Kd(self,V,t):
            # m
            alpha = (V+41.0)/(1-math.exp(-1*(V+41)/10)) 
            beta = 12.5*math.exp(-1*(V+51)/80)
            self.Kd_nTau[t] = 5.0/(alpha+beta)
            n8 = alpha/(alpha+beta)
            self.Kd_n[t] = self.Kd_n[t-1]+(self.timestep*((n8-self.Kd_n[t-1])/self.Kd_nTau[t]))

            self.Kd_g[t] = self.Kd_gMax*math.pow(self.Kd_n[t],4)
            self.Kd_I[t] = self.Kd_g[t]*(self.EK - V)  
            return math.pow(n8,4), n8, alpha  
    def do_CaLow(self,V,t):
            #k
            k8 = 1/(1 + math.exp(-1*(V+61.1)/4.2))
            self.k[t] = self.k[t-1]+((k8-self.k[t-1])/5.0)
            #l
            l8 = 1/(1 + math.exp((V+85.5)/8.5))            
            self.taul = 35 + (20 * math.exp((V+160)/30))/(1+math.exp((V+84)/7.3))
            
            self.l[t] = self.l[t-1]+(self.timestep*(l8-self.l[t-1])/self.taul)
            self.ICaLow[t] = self.gCaLow*math.pow(self.k[t],3)*self.l[t]*(self.ECa-V)
            return k8, l8, math.pow(k8,3)*l8*30
    def do_h(self,V,t): 
            q8 = 1.0/(1.0 + math.exp((V+75.0)/5.5))
            self.Tauq = 1.0/(math.exp((-.086*V)-14.6)+math.exp((.07*V)-1.87))

            self.q[t] = self.q[t-1] + (self.timestep*(q8 - self.q[t-1])/self.Tauq)
            self.Ih[t] = self.gh *self.q[t]* (self.Eh-V)
            return q8, self.Tauq,self.Tauq
    def do_Leak(self,Vs,Vd,t):
            self.IleakS[t] = self.gleakS*(self.Eleak-Vs)
            self.D_Ileak[t] = self.D_gleak*(self.Eleak-Vd)
    def doIO(self):
        for t in range(1,self.duration):
            self.do_Leak(self.VmSoma[t-1],self.VmDend[t-1],t)
            self.do_h(self.VmSoma[t-1],t)
            self.do_CaLow(self.VmSoma[t-1],t)
            self.do_Na(self.VmSoma[t-1],t)
            self.do_Kd(self.VmSoma[t-1],t)
            self.do_CaHigh(self.VmDend[t-1],t)
            self.doCalcium(t)
            self.do_KCa(self.VmDend[t-1],t)
            self.Ids[t] = -1*(self.gint/self.p)*(self.VmSoma[t-1]-self.VmDend[t-1])
            self.Isd[t] = -1*(self.gint/(1-self.p))*(self.VmDend[t-1]-self.VmSoma[t-1])
            self.Im_soma[t]= self.IleakS[t]+self.Na_I[t]+self.Kd_I[t]+self.ICaLow[t]+self.Ih[t]+self.Ids[t]
            self.Im_dend[t]= self.D_Ileak[t]+self.Isd[t]+self.CaHigh_I[t]+self.KCa_I[t]
            self.VmSoma[t] = self.VmSoma[t-1] + (self.timestep*(self.Im_soma[t]/self.Cm))
            self.VmDend[t] = self.VmDend[t-1] + (self.timestep*(self.Im_dend[t]/self.Cm))
            #print(t, self.VmSoma[t],self.VmDend[t],self.Kd_nTau[t],self.CaHigh_Taur[t])
            #print(t,self.VmDend[t],self.Calcium[t],self.KCa_I[t],self.CaHigh_I[t],self.Im_dend[t])
        self.VmSoma[0]=self.VmSoma[self.duration-1]
        self.VmDend[0]=self.VmDend[self.duration-1]
        self.Na_h[0]=self.Na_h[self.duration-1]
        self.Na_hTau[0]=self.Na_hTau[self.duration-1]
        self.Na_m[0]=self.Na_m[self.duration-1]
        self.Kd_n[0]=self.Kd_n[self.duration-1]
        self.k[0]=self.k[self.duration-1]
        self.l[0]=self.l[self.duration-1]
        self.q[0]=self.q[self.duration-1]
        self.CaHigh_r[0]=self.CaHigh_r[self.duration-1]
        self.Calcium[0]=self.Calcium[self.duration-1]
        self.KCa_s[0]=self.KCa_s[self.duration-1]
        return self.VmSoma, self.VmDend

class STGneuron():
    def __init__(self):
        self.FirstTime = 1
        self.duration = 50000
        self.ENa = 50.0
        self.EK = -80.0
        self.ECa = 120.0
        self.ELeak = -50.0
        self.Eh = -20.0
        self.Cm = 0.628  #nFarrads

        self.Im = np.zeros(self.duration)
        self.Vm = np.zeros(self.duration)
        self.timeStep = .05  # 50 microseconds

        # Maximum Conductances # commented value is max from Prinz et al., maximum value tested
        self.Na_gMax = 500.0
        self.Cat_gMax = 12.5
        self.Cas_gMax = 10.0
        self.A_gMax = 50.0
        self.KCa_gMax = 25.0
        self.Kd_gMax =  125.0
        self.h_gMax = .05
        self.gLeak = .05
        # Voltage-gated Na
        self.Na_I = np.zeros(self.duration)
        self.Na_g = np.zeros(self.duration)
        self.Na_m = np.zeros(self.duration)
        self.Na_mTau = np.zeros(self.duration)
        self.Na_h = np.zeros(self.duration)
        self.Na_hTau = np.zeros(self.duration)
        # Transient voltage-gated Ca  
        self.Cat_I = np.zeros(self.duration)
        self.Cat_g = np.zeros(self.duration)
        self.Cat_m = np.zeros(self.duration)
        self.Cat_mTau = np.zeros(self.duration)
        self.Cat_h = np.zeros(self.duration)
        self.Cat_hTau = np.zeros(self.duration)
        # Sustained voltage-gated Ca
        self.Cas_I = np.zeros(self.duration)
        self.Cas_g = np.zeros(self.duration)
        self.Cas_m = np.zeros(self.duration)
        self.Cas_mTau = np.zeros(self.duration)
        self.Cas_h = np.zeros(self.duration)
        self.Cas_hTau = np.zeros(self.duration)
        # A current (transient K)
        self.A_I = np.zeros(self.duration)
        self.A_g = np.zeros(self.duration)
        self.A_m = np.zeros(self.duration)
        self.A_mTau = np.zeros(self.duration)
        self.A_h = np.zeros(self.duration)
        self.A_hTau= np.zeros(self.duration)
        # Calcium-activated K
        self.KCa_I = np.zeros(self.duration)
        self.KCa_g = np.zeros(self.duration)
        self.KCa_m = np.zeros(self.duration)
        self.KCa_mTau = np.zeros(self.duration)
        # Delayed recifier (K)
        self.Kd_I = np.zeros(self.duration)
        self.Kd_g = np.zeros(self.duration)
        self.Kd_m = np.zeros(self.duration)
        self.Kd_mTau = np.zeros(self.duration)
        # hyperpolarization-actived (H) current
        self.h_I =  np.zeros(self.duration)
        self.h_g =  np.zeros(self.duration)
        self.h_m = np.zeros(self.duration)
        self.h_mTau = np.zeros(self.duration)
        # Leak
        self.ILeak = np.zeros(self.duration)
        ## Calcium
        self.Ca = np.zeros(self.duration)
        self.CaTau = 200.0  # 200 ms
        self.f = 14.96 # uM per nA
        self.CaZero = .05  # Internal Calcium goes to .05 uM 

    def RunSim(self,NA,CAT,CAS,A,KCA,KD,H,L):
        self.Na_gMax = NA
        self.Cat_gMax = CAT
        self.Cas_gMax = CAS
        self.A_gMax = A
        self.KCa_gMax = KCA
        self.Kd_gMax = KD
        self.h_gMax = H
        self.gLeak = L
        if self.FirstTime==1:
            self.Vm[0] = self.ENa
            self.FirstTime = 0
        for t in range(1,self.duration):
            self.do_Na(self.Vm[t-1],t)
            self.do_Kd(self.Vm[t-1],t)
            self.do_Leak(self.Vm[t-1],t)
            self.do_A(self.Vm[t-1],t)
            self.do_h(self.Vm[t-1],t)
            self.do_Cas(self.Vm[t-1],t)
            self.do_Cat(self.Vm[t-1],t)
            self.do_Calcium(t)
            self.do_KCa(self.Vm[t-1],t)
            self.Im[t] = self.Na_I[t]+self.Kd_I[t]+self.ILeak[t]+self.A_I[t]+self.h_I[t]+self.Cas_I[t]+self.Cat_I[t]+self.KCa_I[t]
            self.Vm[t] = self.Vm[t-1] + (self.timeStep*(self.Im[t]/self.Cm))

        self.Vm[0]=self.Vm[self.duration-1]
        self.Na_h[0]=self.Na_h[self.duration-1]
        self.Na_hTau[0]=self.Na_hTau[self.duration-1]
        self.Na_m[0]=self.Na_m[self.duration-1]
        self.Na_mTau[0]=self.Na_mTau[self.duration-1]
        self.Kd_m[0]=self.Kd_m[self.duration-1]
        self.Kd_mTau[0]=self.Kd_mTau[self.duration-1]
        self.A_h[0]=self.A_h[self.duration-1]
        self.A_hTau[0]=self.A_hTau[self.duration-1]
        self.A_m[0]=self.A_m[self.duration-1]
        self.A_mTau[0]=self.A_mTau[self.duration-1]
        self.h_m[0]=self.h_m[self.duration-1]
        self.h_mTau[0]=self.h_mTau[self.duration-1]
        self.Cas_h[0]=self.Cas_h[self.duration-1]
        self.Cas_hTau[0]=self.Cas_hTau[self.duration-1]
        self.Cas_m[0]=self.Cas_m[self.duration-1]
        self.Cas_mTau[0]=self.Cas_mTau[self.duration-1]
        self.Cat_h[0]=self.Cat_h[self.duration-1]
        self.Cat_hTau[0]=self.Cat_hTau[self.duration-1]
        self.Cat_m[0]=self.Cat_m[self.duration-1]
        self.Cat_mTau[0]=self.Cat_mTau[self.duration-1]
        self.KCa_m[0]=self.KCa_m[self.duration-1]
        self.KCa_mTau[0]=self.KCa_mTau[self.duration-1]
        self.Ca[0]=self.Ca[self.duration-1]
        return self.Vm,self.Ca

    def do_Na(self,V,t):
        # m
        self.Na_mTau[t] = 2.64-(2.52/(1.0+(math.exp((V+120.0)/-25.0))))
        m8 = 1/(1+math.exp((V+25.5)/-5.29))
        self.Na_m[t] = self.Na_m[t-1]+(self.timeStep*((m8-self.Na_m[t-1])/self.Na_mTau[t]))
        # h
        self.Na_hTau[t]=(1.34/(1+math.exp((V+62.9)/-10.0)))
        #self.Na_hTau[t]=1.5 +(1/(1+math.exp((V+34.9)/3.6)))
        h8 = 1/(1+math.exp((V+48.9)/5.18))
        self.Na_h[t] = self.Na_h[t-1]+(self.timeStep*((h8-self.Na_h[t-1])/self.Na_hTau[t]))
        
        self.Na_g[t] = self.Na_gMax*math.pow(self.Na_m[t],3)*self.Na_h[t]
        self.Na_I[t] = self.Na_g[t]*(self.ENa - V)
        return math.pow(m8,3), h8, math.pow(m8,3)*h8*self.Na_gMax
    def do_Kd(self,V,t):
        # m
        self.Kd_mTau[t] = 14.4-(12.8/(1+(math.exp((V+28.3)/-19.2))))
        m8 = 1/(1+math.exp((V+12.3)/-11.8))
        self.Kd_m[t] = self.Kd_m[t-1]+(self.timeStep*((m8-self.Kd_m[t-1])/self.Kd_mTau[t]))
        
        self.Kd_g[t] = self.Kd_gMax*math.pow(self.Kd_m[t],4)
        self.Kd_I[t] = self.Kd_g[t]*(self.EK - V)
        return math.pow(m8,4), m8, (math.pow(m8,4)*self.Kd_gMax)/100
    def do_A(self,V,t):
        # m
        self.A_mTau[t] = 23.2-(20.8/(1.0+(math.exp((V+32.9)/-15.2))))
        m8 = 1/(1+math.exp((V+27.2)/-8.7))
        self.A_m[t] = self.A_m[t-1]+(self.timeStep*((m8-self.A_m[t-1])/self.A_mTau[t]))
        # h
        self.A_hTau[t]=77.2-(58.4/(1+math.exp((V+38.9)/-26.5)))
        h8 = 1/(1+math.exp((V+56.9)/4.9))
        self.A_h[t] = self.A_h[t-1]+(self.timeStep*((h8-self.A_h[t-1])/self.A_hTau[t]))
        
        self.A_g[t] = self.A_gMax*math.pow(self.A_m[t],3)*self.A_h[t]
        self.A_I[t] = self.A_g[t]*(self.EK - V)
        return math.pow(m8,3), h8, math.pow(m8,3)*h8*self.A_gMax*10
    def do_h(self,V,t):
        # m
        self.h_mTau[t] = 2/(math.exp((V+169.7)/-11.6)+math.exp((V-26.7)/14.3))
        m8 = 1/(1+math.exp((V+75.0)/5.5))
        self.h_m[t] = self.h_m[t-1]+(self.timeStep*((m8-self.h_m[t-1])/self.h_mTau[t]))
        
        self.h_g[t] = self.h_gMax*self.h_m[t]
        self.h_I[t] = self.h_g[t]*(self.Eh - V)
        return m8, m8, m8
    def do_Cas(self,V,t):
        # m
        self.Cas_mTau[t] = 2.8+(14.0/((math.exp((V+27.0)/10.0))+(math.exp((V+70.0)/-13.0))))
        m8 = 1/(1+math.exp((V+33.0)/-8.1))
        self.Cas_m[t] = self.Cas_m[t-1]+(self.timeStep*((m8-self.Cas_m[t-1])/self.Cas_mTau[t]))
        # h
        self.Cas_hTau[t]=120+(300.0/(math.exp((V+55.0)/9.0))+math.exp((V+65.0)/-16.0))
        h8 = 1/(1+math.exp((V+60.0)/6.2))
        self.Cas_h[t] = self.Cas_h[t-1]+(self.timeStep*((h8-self.Cas_h[t-1])/self.Cas_hTau[t]))
        
        self.Cas_g[t] = self.Cas_gMax*math.pow(self.Cas_m[t],3)*self.Cas_h[t]
        self.Cas_I[t] = self.Cas_g[t]*(self.ECa - V)
        return math.pow(m8,3), h8, math.pow(m8,3)*h8*self.Cas_gMax*10
    def do_Cat(self,V,t):
        # m
        self.Cat_mTau[t] = 43.4-(42.6/(1+(math.exp((V+68.1)/-20.5))))
        m8 = 1/(1+math.exp((V+27.1)/-7.2))
        self.Cat_m[t] = self.Cat_m[t-1]+(self.timeStep*((m8-self.Cat_m[t-1])/self.Cat_mTau[t]))
        # h
        self.Cat_hTau[t]=210-(179.6/(1+math.exp((V+55.0)/-16.9)))
        h8 = 1/(1+math.exp((V+32.1)/5.5))
        self.Cat_h[t] = self.Cat_h[t-1]+(self.timeStep*((h8-self.Cat_h[t-1])/self.Cat_hTau[t]))

        self.Cat_g[t] = self.Cat_gMax*math.pow(self.Cat_m[t],3)*self.Cat_h[t]
        self.Cat_I[t] = self.Cat_g[t]*(self.ECa - V)
        return math.pow(m8,3), h8, math.pow(m8,3)*h8*self.Cat_gMax
    def do_KCa(self,V,t):
        # m
        self.KCa_mTau[t] = 180.6-(150.2/(1+(math.exp((V+46.0)/-22.7))))
        m8 = (self.Ca[t-1]/(self.Ca[t-1] + 3.0))*(1/(1+math.exp((V+28.3)/-12.6)))
        self.KCa_m[t] = self.KCa_m[t-1]+(self.timeStep*((m8-self.KCa_m[t-1])/self.KCa_mTau[t]))
        
        self.KCa_g[t] = self.KCa_gMax*math.pow(self.KCa_m[t],4)
        self.KCa_I[t] = self.KCa_g[t]*(self.EK - V)
    def do_Calcium(self,t):
        dCa = self.timeStep*(self.f*(self.Cat_I[t-1]+self.Cas_I[t-1])-(self.Ca[t-1]-self.CaZero))
        self.Ca[t]=self.Ca[t-1]+dCa
    def do_Leak(self,V,t):
        self.ILeak[t] = self.gLeak*(self.ELeak-V)

class IAFneuron():

    def __init__(self):
        self.duration = 2500
        self.timeStep = 1
        self.Vm = np.zeros(self.duration)
        self.Thresh = np.zeros(self.duration)
        self.AHP = np.zeros(self.duration)
        self.Calcium = np.zeros(self.duration)
        self.KCa = np.zeros(self.duration)
        self.spikes = np.zeros(self.duration)
        self.Capacitance = 1
        # parameters
        self.gLeak = .01
        self.ENa = 50.0
        self.EK = -80.0
        self.Eleak = -60.0
        #### Threshold
        self.threshBase = -65.0
        self.threshMax = 0.0
        self.ThrTau = 2.0  # threshold decay time constant in ms
        self.ThrDecay = 1-(math.exp(-1/self.ThrTau))
        #### Calcium
        self.CalciumTau = 200
        self.CalciumDecay = math.exp(-1/self.CalciumTau)
        self.CalciumInc = .1
        #### Calcium activated K
        self.KCaTau = 10
        self.KCaDecayTau = 50
        self.KCaDecay = 100
        #initial values
        self.Vm[0] = self.EK
        self.Thresh[0] = self.threshBase
        self.AHP[0] = 0.0
        self.Calcium[0] = 0.0
        self.KCa[0] = 0.0
        self.spikes[0] = 0
    def RunSim(self):
        for t in range(1, self.duration):
            self.DoTimeStep(t)
        return self.Vm, self.spikes
    def DoTimeStep(self,t):
        self.Vm[t] = self.Vm[t-1] + (self.gLeak*(self.Eleak-self.Vm[t-1]))+(self.AHP[t-1]*(self.EK-self.Vm[t-1]))+(self.KCa[t-1]*(self.EK-self.Vm[t-1]))/self.Capacitance
        if (self.Vm[t] > self.Thresh[t-1]):
            self.spikes[t] = 1
            self.Thresh[t] = self.threshMax 
            self.Calcium[t] = self.Calcium[t-1]+self.CalciumInc*(1-self.Calcium[t-1])
        else:
            self.spikes[t] = 0
            self.Thresh[t] = self.Thresh[t-1] + (self.ThrDecay * (self.threshBase-self.Thresh[t-1]))
            self.AHP[t] = self.AHP[t-1]*.6
            self.Calcium[t] = self.Calcium[t-1]*self.CalciumDecay        
        k8 = (self.Calcium[t]-.2)*2.5
        if k8 < 0:k8=0
        self.KCa[t] = self.KCa[t-1]+((k8-self.KCa[t-1])*.005)
        if t == self.duration-1:
            self.Vm[0] = self.Vm[t]
            self.Thresh[0] = self.Thresh[t]
            self.AHP[0] = self.AHP[t]
            self.Calcium[0] = self.Calcium[t]
            self.KCa[0] = self.KCa[t]
            self.spikes[0] = self.spikes[t]   
        return self.Vm[t],self.spikes[t],self.Calcium[t],self.KCa[t]