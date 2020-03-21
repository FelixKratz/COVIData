import numpy as np 
import pandas as pd

#Tinf und Tinc in days !!!
def model(R0,Rt,Tinf,Tinc,Iday):
    days = 10
    S0 = 83000000 # population (83mio)
    E0 = 0 # exposed
    I0 = 1 # intial infections
    Re0 = 0 # removed
    series = pd.DataFrame({"S":[S0],"E":[E0],"I":[I0],"R":[Re0]})
    actual = pd.DataFrame({"S":[S0],"E":[E0],"I":[I0],"R":[Re0]})
    for i in range(days):
        S = actual.S - R0/Tinf*actual.I*actual.S
        E = actual.E + R0/Tinf*actual.I*actual.S - 1/Tinc*actual.E
        I = actual.I + 1/Tinc*actual.E - 1/Tinf*actual.I
        R = actual.R + 1/Tinf*actual.I
        if S.values<0:
            S = 0
        if E.values<0:
            E = 0
        if I.values<0:
            I = 0
        if R.values<0:
            R = 0 
        actual = pd.DataFrame({"S":S,"E":E,"I":I,"R":R})
        series = series.append(actual)
    print(series)
    return series


model(2.2,2.2,3.,5.,12.)