from dataHandler import DataHandler
from leastSquares import *
from SEIRmodel import SEIRModel
import sys

sys.setrecursionlimit(int(1e8))

dataHandler = DataHandler()
dataHandler.loadData()

germanData = dataHandler.filterForCountry("Germany")

fitParamsToModel(germanData['confirmed'][30:],
                 initialGuess={'beta': 642.3430438150659, 'gamma': 3.5462661166540026, 'sigma': 0.0016878787803937588, 'mu': 0, 'nu': 0, 'dt': 0.1, 'S0': 83000000.0, 'E0': 0, 'I0': 249.0634121560787, 'Re0': 0, 'darkrate': 0.05, 'hardrate': 0.154, 'deathrate': 0.034},
                  parametersToFit=['beta', 'gamma', 'sigma', 'I0'])
#{'beta': 2.6611534876710494, 'gamma': 1.1193829408556317, 'sigma': 0.14324823943299667, 'mu': 0, 'nu': 0, 'dt': 0.1, 'S0': 83000000.0, 'E0': 0, 'I0': 21.018772332969615, 'Re0': 0, 'darkrate': 0.05, 'hardrate': 0.154, 'deathrate': 0.034}

# actions=[{'date_of_action':54,
# 'beta':0.58,
# 'gamma':0.7835539610885016,
# 'sigma':19.559902079217732,
# 'mu':0,
# 'nu':0},
# {'date_of_action':62,
# 'beta':0.5,
# 'gamma':0.7835539610885016,
# 'sigma':19.559902079217732,
# 'mu':0,
# 'nu':0}
# ],
