import numpy as np
from SEIRmodel import SEIRModel

def absoluteSquareError(simulation, reality):
    simulation = np.array(simulation)
    reality = np.array(reality)

    if (len(simulation) != len(reality)):
        print("Error: Non matching input dimensions in absoluteSquareError()!")

    print(simulation)
    print(reality)
    return sum((simulation - reality)**2)

def squareErrorByElement(simulation, reality):
    reality = np.array(reality)

    if (len(simulation) != len(reality)):
        print("Error: Non matching input dimensions in absoluteSquareError()!")

    return (simulation - reality)**2

def fitParamsToModel(reality, initialGuess, parametersToFit):
    DX = 1e-6

    initialModel = SEIRModel(initialGuess)
    initialModel.compute(days=len(reality))
    initialSim = initialModel.get_daily_numbers()['D'].to_numpy()
    initialError = absoluteSquareError(initialSim, reality)
    F = squareErrorByElement(initialSim, reality)
    jacobian = np.zeros((len(parametersToFit), len(reality)))

    i = 0
    for p in parametersToFit:
        error = [[], []]
        for j in [-1, 1]:
            displacement = initialGuess
            displacement[p] += DX * j
            displacedModel = SEIRModel(displacement)
            displacedModel.compute(days=len(reality))
            displacedSimulation = displacedModel.get_daily_numbers()['D'].to_numpy()
            error[(j + 1) // 2] = squareErrorByElement(displacedSimulation, reality)
        jacobian[i] = (error[0] - error[1]) / (2* DX)
        i+=1

    dX = - np.array(np.linalg.lstsq(jacobian.T, -F)[0])

    dX = dX / np.sqrt(sum(dX**2)) * 1e-1

    i = 0
    for p in parametersToFit:
        initialGuess[p] += dX[i]
        i += 1

    finalModel = SEIRModel(initialGuess)
    finalModel.compute(days=len(reality))
    finalSim = finalModel.get_daily_numbers()['D'].to_numpy()
    finalError = absoluteSquareError(finalSim, reality)

    print("Initial Error: ", initialError)
    print("Final Error: ", finalError)
    print("Parameter: ", initialGuess)
    if not finalError < 1e-8:
        fitParamsToModel(reality, initialGuess, parametersToFit)
    else:
        print("Final Params: ", initialGuess)
