import numpy as np
from SEIRmodel import SEIRModel

def absoluteSquareError(simulation, reality):
    simulation = np.array(simulation)
    reality = np.array(reality)

    if (len(simulation) != len(reality)):
        print("Error: Non matching input dimensions in absoluteSquareError()!")

    print(simulation)
    print(reality)
    return sum((np.log(simulation) - np.log(reality))**2)

def squareErrorByElement(simulation, reality):
    reality = np.array(reality)

    if (len(simulation) != len(reality)):
        print("Error: Non matching input dimensions in absoluteSquareError()!")

    return (np.log(simulation) - np.log(reality))**2

def fitParamsToModel(reality, initialGuess, parametersToFit, actions=None):
    DX = 1e-3
    withAction = False
    if actions != None and len(actions) > 0:
        withAction = True
    initialModel = SEIRModel(initialGuess, actions)
    initialSim = initialModel.compute(days=len(reality), with_action = withAction)['D']
    initialError = absoluteSquareError(initialSim, reality)
    F = squareErrorByElement(initialSim, reality)
    jacobian = np.zeros((len(parametersToFit), len(reality)))

    i = 0
    for p in parametersToFit:
        error = [[], []]
        for j in [-1, 1]:
            displacement = initialGuess
            if (displacement[p] + DX * j > 0):
                displacement[p] += DX * j
            displacedModel = SEIRModel(displacement, actions)
            displacedSimulation = displacedModel.compute(days=len(reality), with_action = withAction)['D']
            error[(j + 1) // 2] = squareErrorByElement(displacedSimulation, reality)
        jacobian[i] = (error[0] - error[1]) / (2* DX)
        i+=1

    dX = - np.array(np.linalg.lstsq(jacobian.T, -F)[0])

    dX = dX / np.sqrt(sum(dX**2)) * 1e-2

    i = 0
    for p in parametersToFit:
        initialGuess[p] += dX[i]
        if initialGuess[p] < 0:
            initialGuess[p] = 0
        i += 1

    finalModel = SEIRModel(initialGuess, actions)
    finalSim = finalModel.compute(days=len(reality), with_action = withAction)['D']
    finalError = absoluteSquareError(finalSim, reality)

    print("Initial Error: ", initialError)
    print("Final Error: ", finalError)
    print("Parameter: ", initialGuess)
    if not finalError < 1e-8:
        fitParamsToModel(reality, initialGuess, parametersToFit, actions=actions)
    else:
        print("Final Params: ", initialGuess)
