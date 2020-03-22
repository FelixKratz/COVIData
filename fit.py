from dataHandler import DataHandler
from leastSquares import *
from SEIRmodel import SEIRModel

dataHandler = DataHandler()
dataHandler.loadData()

germanData = dataHandler.filterForCountry("Germany")

fitParamsToModel(germanData['confirmed'][4:45],
                 initialGuess={'beta': 0.016860477770656995,  # The parameter controlling how often a susceptible-infected contact results in a new exposure.
                               'gamma':0.056376046656360854,  # The rate an infected recovers and moves into the resistant phase.
                               'sigma': 20.293257546664027, # The rate at which an exposed person becomes infective.
                               'mu': 0,      # The natural mortality rate (this is unrelated to disease). This models a population of a constant size,
                               'nu': 0,      # Ich glaube Immunrate. Wie viele Leute von sich aus Immun sind gegen COVID19
                               'dt': 0.1,
                               'S0': 83e6,
                               'E0': 0,
                               'I0': 81.68139377344086,
                               'Re0': 0,
                               'darkrate': 0.05, # erstmal China studie # Quelle: Linton MN, Kobayashi T, Yang Y, Hayashi K, Akhmetzhanov RA, Jung S-m, et al. Incubation Period and Other Epidemiological Characteristics of 2019 Novel Coronavirus Infections with Right Truncation: A Statistical Analysis of Publicly Available Case Data. Journal of clinical medicine. 2020.
                               'hardrate': 0.154, # WHO studie:  Novel Coronavirus (2019-nCoV). (PDF; 0,9 MB) Situation Report – 18. WHO, 7. Februar 2020, abgerufen am 8. Februar 2020.
                               'deathrate': 0.034},
                  parametersToFit=['beta', 'gamma', 'sigma', 'I0'])
