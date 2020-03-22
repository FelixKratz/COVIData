from dataHandler import DataHandler
from leastSquares import *
from SEIRmodel import SEIRModel

dataHandler = DataHandler()
dataHandler.loadData()

germanData = dataHandler.filterForCountry("Germany")

fitParamsToModel(germanData['confirmed'][25:],
                 initialGuess={'beta': 0.10719316873333488, 'gamma': 0, 'sigma': 20.205025048814136, 'mu': 0, 'nu': 0, 'dt': 0.1,
                               'S0': 83000000.0, 'E0': 0, 'I0': 102.58042879494874, 'Re0': 0, 'darkrate': 0.05, 'hardrate': 0.154, 'deathrate': 0.034},
                  parametersToFit=['beta', 'gamma', 'sigma', 'I0'])
