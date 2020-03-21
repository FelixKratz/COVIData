import numpy as np 
import pandas as pd

#Tinf und Tinc in days !!!
def model(params):
    R0 = params[0]
    Rt = params[1]
    Tinf = params[2]
    Tinc = params[3]
    dt = 0.001
    days = 10
    S0 = 83000000 # population (83mio)
    E0 = 0 # exposed
    I0 = 1 # intial infections
    Re0 = 0 # removed
    series = pd.DataFrame({"S":[S0],"E":[E0],"I":[I0],"R":[Re0]})
    actual = pd.DataFrame({"S":[S0],"E":[E0],"I":[I0],"R":[Re0]})
    for i in range(days):
        S = actual.S - R0/Tinf*actual.I*actual.S*dt
        E = actual.E + R0/Tinf*actual.I*actual.S*dt - 1/Tinc*actual.E*dt
        I = actual.I + 1/Tinc*actual.E*dt - 1/Tinf*actual.I*dt
        R = actual.R + 1/Tinf*actual.I*dt
        if S.values<1:
            S = 0
        if E.values<1:
            E = 0
        if I.values<1:
            I = 0
        if R.values<1:
            R = 0 
        actual = pd.DataFrame({"S":S,"E":E,"I":I,"R":R})
        series = series.append(actual)
    print(series)
    return series


ser = model([2.2,2.2,3.,5.,1.])
ser.I.plot()