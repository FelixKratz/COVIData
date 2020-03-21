import numpy as np
import pandas as pd

class SEIRModel:
    def __init__(self, params):
        self.params = params
        self.series = pd.DataFrame({"S":[self.params['S0']],
                                    "E":[self.params['E0']],
                                    "I":[self.params['I0']],
                                    "R":[self.params['Re0']],
                                    "N":[self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0']],
                                    "D":[self.params["I0"]*self.params["darkrate"]],
                                    "hard_course":[self.params["I0"]*self.params["darkrate"]*self.params["hardrate"]],
                                    "deadly_course":[self.params["I0"]*self.params["darkrate"]*self.params["deathrate"]]})

    def compute(self, days):
        #calculates the next $steps$ steps and gives back the whole series
        actual = self.series.iloc[-1,:]
        for _ in range(days-1):
            for _ in range(round(1/self.params["dt"])):
                actual = pd.Series({"S": actual.S + ( self.params['mu']*(actual.N-actual.S) - self.params['beta']*actual.I*actual.S/actual.N - self.params['nu']*actual.S )*self.params['dt'],
                                        "E": actual.E + ( self.params['beta']*actual.I*actual.S/actual.N - (self.params['mu']+self.params['sigma'])*actual.E ) * self.params['dt'],
                                        "I": actual.I + ( self.params['sigma']*actual.E - (self.params['mu']+self.params['gamma'])*actual.I ) * self.params['dt'],
                                        "R": actual.R + ( self.params['gamma']*actual.I - self.params['mu']*actual.R + self.params['nu']*actual.S) * self.params['dt'],
                                        "N": 0 ,
                                        "D": 0,
                                        "hard_course": 0,
                                        "deadly_course": 0})

                actual.N = actual.S + actual.E + actual.I + actual.R
                actual.D = actual.I*self.params['darkrate']
                actual.hard_course = actual.I*self.params['darkrate']*self.params['hardrate']
                actual.deadly_course = actual.I*self.params['darkrate']*self.params['deathrate']
            self.series = self.series.append(actual,ignore_index=True)
        return self.series

    def compute_faster(self,days):
        actual = self.series.iloc[-1,:]
        for _ in range(days-1):
            for _ in range(round(1/self.params["dt"])):
                actual = pd.Series({"S": actual.S + ( self.params['mu']*(actual.N-actual.S) - self.params['beta']*actual.I*actual.S/actual.N - self.params['nu']*actual.S )*self.params['dt'],
                                        "E": actual.E + ( self.params['beta']*actual.I*actual.S/actual.N - (self.params['mu']+self.params['sigma'])*actual.E ) * self.params['dt'],
                                        "I": actual.I + ( self.params['sigma']*actual.E - (self.params['mu']+self.params['gamma'])*actual.I ) * self.params['dt'],
                                        "R": actual.R + ( self.params['gamma']*actual.I - self.params['mu']*actual.R + self.params['nu']*actual.S) * self.params['dt'],
                                        "N": 0 ,
                                        "D": 0,
                                        "hard_course": 0,
                                        "deadly_course": 0})

                actual.N = actual.S + actual.E + actual.I + actual.R
                #actual.D = actual.I*self.params['darkrate']
                #actual.hard_course = actual.I*self.params['darkrate']*self.params['hardrate']
                #actual.deadly_course = actual.I*self.params['darkrate']*self.params['deathrate']
            self.series = self.series.append(actual,ignore_index=True)
        return self.series

    def reset(self):
        # resets the series
        self.series =  pd.DataFrame({"S":[self.params['S0']],
                                    "E":[self.params['E0']],
                                    "I":[self.params['I0']],
                                    "R":[self.params['Re0']],
                                    "N":[self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0']],
                                    "D":[self.params["I0"]*self.params["darkrate"]],
                                    "hard_course":[self.params["I0"]*self.params["darkrate"]*self.params["hardrate"]],
                                    "deadly_course":[self.params["I0"]*self.params["darkrate"]*self.params["deathrate"]]})


if __name__ == "__main__" :
    model = SEIRModel({
                    'beta': 0.6,  # The parameter controlling how often a susceptible-infected contact results in a new exposure.
                    'gamma':0.2,  # The rate an infected recovers and moves into the resistant phase.
                    'sigma': 0.5, # The rate at which an exposed person becomes infective.
                    'mu': 0,      # The natural mortality rate (this is unrelated to disease). This models a population of a constant size,
                    'nu': 0,      # Ich glaube Immunrate. Wie viele Leute von sich aus Immun sind gegen COVID19
                    'dt': 0.1,
                    'S0': 83e6,
                    'E0': 0,
                    'I0': 20,
                    'Re0': 0,
                    'darkrate': 0.05, # erstmal China studie # Quelle: Linton MN, Kobayashi T, Yang Y, Hayashi K, Akhmetzhanov RA, Jung S-m, et al. Incubation Period and Other Epidemiological Characteristics of 2019 Novel Coronavirus Infections with Right Truncation: A Statistical Analysis of Publicly Available Case Data. Journal of clinical medicine. 2020.
                    'hardrate': 0.154, # WHO studie:  Novel Coronavirus (2019-nCoV). (PDF; 0,9 MB) Situation Report – 18. WHO, 7. Februar 2020, abgerufen am 8. Februar 2020.
                    'deathrate': 0.034 # WHO :  Eröffnungsrede des WHO-Generaldirektors – Pressekonferenz zu COVID-19 – 3. März 2020. WHO, 3. März 2020, abgerufen am 6. März 2020 (englisch).
                    })

    prediction = model.compute(days=16)
    print(model.get_daily_numbers()['D'])
