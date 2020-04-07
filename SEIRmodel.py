import numpy as np
import pandas as pd
from dataHandler import DataHandler
import matplotlib.pyplot as plt

class SEIRModel:
    def __init__(self, params, actions=None):
        self.params = params
        self.actual = []
        self.actions = actions
        self.series = []
        self.reset()

    def compute(self, days, with_action = False):
        for i in range(days-1):
            for _ in range(round(1/self.params["dt"])):
                params = []
                actionTriggered = False
                if with_action:
                    j = 0
                    actionIndex = -1
                    for k in range(len(self.actions)):
                        j_tmp = self.actions[k]['date_of_action']
                        if i >= j_tmp and j_tmp > j:
                            j = j_tmp
                            actionIndex = k

                    if (actionIndex >= 0):
                        params = self.actions[actionIndex]
                        actionTriggered = True

                if not actionTriggered:
                    params = self.params

                # 0 = S; 1 = E; 2 = I; 3 = R; 4 = N; 5 = (D)etected
                self.actual[0] = self.actual[0] + ( params['mu']*(self.actual[4]-self.actual[0])
                                - params['beta']*self.actual[2]*self.actual[0]/self.actual[4]
                                - params['nu']*self.actual[0] )*self.params['dt']
                self.actual[1] = self.actual[1] + ( params['beta']*self.actual[2]*self.actual[0]/self.actual[4]
                                - (params['mu']+params['sigma'])*self.actual[1] ) * self.params['dt']

                self.actual[2] = self.actual[2] + ( params['sigma']*self.actual[1]
                                - (params['mu']+params['gamma'])*self.actual[2] ) * self.params['dt']

                self.actual[3] = self.actual[3] + ( params['gamma']*self.actual[2] - params['mu']*self.actual[3]
                                + params['nu']*self.actual[0]) * self.params['dt']

                self.actual[4] = self.actual[0] + self.actual[1] + self.actual[2] + self.actual[3]
                self.actual[5] = self.actual[2]*self.params['darkrate'] + self.actual[3]*self.params['darkrate']

            self.series.append(self.actual[:])
        self.series = np.array(self.series)
        return {"S": self.series.T[0], "E": self.series.T[1], "I": self.series.T[2], "R":  self.series.T[3], "N": self.series.T[4], "D": self.series.T[5], "deadly_course": self.series.T[3]*self.params['deathrate'], "hard_course": self.series.T[3]*self.params['hardrate']}

    def reset(self):
        # resets the series
        self.actual = [self.params['S0'],
                       self.params['E0'],
                       self.params['I0'],
                       self.params['Re0'],
                       self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0'],
                       (self.params["I0"] + self.params['Re0'])*self.params["darkrate"]]
        self.series = [self.actual[:]]

if __name__ == "__main__" :
    model = SEIRModel({'beta': 642.3430438150659, 'gamma': 3.5462661166540026, 'sigma': 0.0016878787803937588, 'mu': 0, 'nu': 0, 'dt': 0.1, 'S0': 83000000.0, 'E0': 0, 'I0': 249.0634121560787, 'Re0': 0, 'darkrate': 0.05, 'hardrate': 0.154, 'deathrate': 0.034},
                       [{'date_of_action':54,
                       'beta':0.58,
                       'gamma':0.7835539610885016,
                       'sigma':19.559902079217732,
                       'mu':0,
                       'nu':0},
                       {'date_of_action':62,
                       'beta':0.5,
                       'gamma':0.7835539610885016,
                       'sigma':19.559902079217732,
                       'mu':0,
                       'nu':0}
                       ])
    #{'beta': 0.3920097374378698, 'gamma': 0.4658171977205657, 'sigma': 19.850638745563344, 'mu': 0, 'nu': 0, 'dt': 0.1, 'S0': 83000000.0, 'E0': 0, 'I0': 36.51139408522852, 'Re0': 0, 'darkrate': 0.05, 'hardrate': 0.154, 'deathrate': 0.034}
    prediction = model.compute(days=50, with_action=False)['D']
    print(prediction)
    dataHandler = DataHandler()
    dataHandler.loadData()

    germanData = dataHandler.filterForCountry("Germany")
    germanData = germanData['confirmed'][30:]
    print(germanData)
    x = np.linspace(1, len(prediction), len(prediction))
    plt.plot(x, prediction,"b.", label="Prediction")
    x2 = np.linspace(1, len(germanData), len(germanData))
    plt.plot(x2, germanData, "r.", label="Data")
    plt.yscale("log")
    #plt.ylim(-100, 100)
    plt.legend(loc="best")
    plt.show()
