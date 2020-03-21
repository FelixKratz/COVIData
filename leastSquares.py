import numpy as np
from SEIRmodel import SEIRModel

def absoluteSquareError(simulation, reality):
    simulation = np.array(simulation)
    reality = np.array(reality)

    if (len(simulation) != len(reality)):
        print("Error: Non matching input dimensions in absoluteSquareError()!")

    return sum((simulation - reality)**2)

def fitParamsToModel(reality, initialGuess, paramsToFit):
    model = SEIRModel(initialGuess)
    simulation = model.compute(steps=len(reality))
