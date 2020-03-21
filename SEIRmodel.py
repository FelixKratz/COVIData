import numpy as np
import pandas as pd

class SEIRModel:
    def __init__(self, params):
        self.params = params

    def compute(self, steps):
        series = pd.DataFrame({"S":[self.params['S0']],"E":[self.params['E0']],"I":[self.params['I0']],"R":[self.params['Re0']],"N":[self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0']]})
        actual = pd.DataFrame({"S":[self.params['S0']],"E":[self.params['E0']],"I":[self.params['I0']],"R":[self.params['Re0']],"N":[self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0']]})
        for _ in range(steps - 1):
            S = actual.S + ( self.params['mu']*(actual.N-actual.S) - self.params['beta']*actual.I*actual.S/actual.N - self.params['nu']*actual.S )*self.params['dt']
            E = actual.E + ( self.params['beta']*actual.I*actual.S/actual.N - (self.params['mu']+self.params['sigma'])*actual.E ) * self.params['dt']
            I = actual.I + ( self.params['sigma']*actual.E - (self.params['mu']+self.params['gamma'])*actual.I ) * self.params['dt']
            R = actual.R + ( self.params['gamma']*actual.I - self.params['mu']*actual.R + self.params['nu']*actual.S) * self.params['dt']
            #if S.values < 1:
            #    S = 0
            #if E.values < 1:
            #    E = 0
            #if I.values < 1:
            #    I = 0
            #if R.values < 1:
            #    R = 0
            actual = pd.DataFrame({"S":S,"E":E,"I":I,"R":R,"N":S+E+I+R})
            series = series.append(actual)
        return series

model = SEIRModel({
                    'beta': 0.9,
                    'gamma':0.2,
                    'sigma': 0.5,
                    'mu': 0,
                    'nu': 0,
                    'dt': 0.1,
                    'S0': 30,
                    'E0': 0,
                    'I0': 1,
                    'Re0': 0})

prediction = model.compute(steps=150)
print(prediction)
