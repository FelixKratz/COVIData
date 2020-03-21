import numpy as np
import pandas as pd

class SEIRModel:
    def __init__(self, params):
        self.params = params

    def compute(self, steps):
        series = pd.DataFrame({"S":[self.params['S0']],"E":[self.params['E0']],"I":[self.params['I0']],"R":[self.params['Re0']]})
        actual = pd.DataFrame({"S":[self.params['S0']],"E":[self.params['E0']],"I":[self.params['I0']],"R":[self.params['Re0']]})
        for _ in range(steps - 1):
            S = actual.S - self.params['R0']/self.params['Tinf']*actual.I*actual.S*self.params['dt']
            E = actual.E + self.params['R0']/self.params['Tinf']*actual.I*actual.S*self.params['dt'] - 1/self.params['Tinc']*actual.E*self.params['dt']
            I = actual.I + 1/self.params['Tinc']*actual.E*self.params['dt'] - 1/self.params['Tinf']*actual.I*self.params['dt']
            R = actual.R + 1/self.params['Tinf']*actual.I*self.params['dt']
            if S.values < 1:
                S = 0
            if E.values < 1:
                E = 0
            if I.values < 1:
                I = 0
            if R.values < 1:
                R = 0
            actual = pd.DataFrame({"S":S,"E":E,"I":I,"R":R})
            series = series.append(actual)
        return series

model = SEIRModel({'R0': 2.2,
                   'Rt': 2.2,
                   'Tinf': 3.0,
                   'Tinc': 5.0,
                   'dt': 0.001,
                   'S0': 83e6,
                   'E0': 0,
                   'I0': 1,
                   'Re0': 0})

prediction = model.compute(steps=10)
print(prediction)
