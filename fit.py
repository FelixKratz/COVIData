from dataHandler import DataHandler
from leastSquares import *
from SEIRmodel import SEIRModel

dataHandler = DataHandler()
dataHandler.loadData()

germanData = dataHandler.filterForCountry("Germany")

fitParamsToModel(germanData['confirmed'][4:],
                 initialGuess={'beta': 0.4458832735928616, 'gamma': 0.04142817668313051, 'sigma': 0.13654249480116884, 'mu': 0, 'nu': 0, 'dt': 0.1,
                               'S0': 83000000.0, 'E0': 0, 'I0': 46.53585481679889, 'Re0': 0, 'darkrate': 0.05, 'hardrate': 0.154, 'deathrate': 0.034},
                  parametersToFit=['beta', 'gamma', 'sigma', 'I0'])
