import numpy as np
import pandas as pd

class SEIRModel:
    def __init__(self, params, params2=None):
        self.params = params
        self.params2 = params2
        self.series = pd.DataFrame({"S":[self.params['S0']],
                                    "E":[self.params['E0']],
                                    "I":[self.params['I0']],
                                    "R":[self.params['Re0']],
                                    "N":[self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0']],
                                    "D":[self.params["I0"]*self.params["darkrate"]],
                                    "hard_course":[self.params["I0"]*self.params["darkrate"]*self.params["hardrate"]],
                                    "deadly_course":[self.params["I0"]*self.params["darkrate"]*self.params["deathrate"]]})
        self.actual = None

    def set_actual(self,params):
        self.actual = pd.Series({"S": self.actual.S + ( params['mu']*(self.actual.N-self.actual.S) - params['beta']*self.actual.I*self.actual.S/self.actual.N - params['nu']*self.actual.S )*self.params['dt'],
                        "E": self.actual.E + ( params['beta']*self.actual.I*self.actual.S/self.actual.N - (params['mu']+params['sigma'])*self.actual.E ) * self.params['dt'],
                        "I": self.actual.I + ( params['sigma']*self.actual.E - (params['mu']+params['gamma'])*self.actual.I ) * self.params['dt'],
                        "R": self.actual.R + ( params['gamma']*self.actual.I - params['mu']*self.actual.R + params['nu']*self.actual.S) * self.params['dt'],
                        "N": None ,
                        "D": None,
                        "hard_course": None,
                        "deadly_course": None})


    def compute(self, days, with_action = False):
        #calculates the next $steps$ steps and gives back the whole series
        self.actual = self.series.iloc[-1,:]

        for i in range(days-1):
            for _ in range(round(1/self.params["dt"])):
                if with_action and self.params2['date_of_action']<=i:
                    self.set_actual(self.params2)
                else:
                    self.set_actual(self.params)

                self.actual.N = self.actual.S + self.actual.E + self.actual.I + self.actual.R
                self.actual.D = self.actual.I*self.params['darkrate'] + self.actual.R*self.params['darkrate']
                self.actual.hard_course = self.actual.I*self.params['darkrate']*self.params['hardrate']
                self.actual.deadly_course = self.actual.R*self.params['darkrate']*self.params['deathrate']
            self.series = self.series.append(self.actual,ignore_index=True)
        return self.series

    def compute_faster(self,days,with_action=False):
        self.actual = self.series.iloc[-1,:]
        for _ in range(days-1):
            for _ in range(round(1/self.params["dt"])):
                if with_action and self.params2['date_of_action']<=days:
                    self.set_actual(self.params2)
                else:
                    self.set_actual(self.params)
                self.actual.N = self.actual.S + self.actual.E + self.actual.I + self.actual.R
                self.actual.D = self.actual.I*self.params['darkrate'] + self.actual.R*self.params['darkrate']
                #
                #
            self.series = self.series.append(self.actual,ignore_index=True)
        return self.series

    def reset(self):
        # resets the series
        self.series =  pd.DataFrame({"S":[self.params['S0']],
                                    "E":[self.params['E0']],
                                    "I":[self.params['I0']],
                                    "R":[self.params['Re0']],
                                    "N":[self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0']],
                                    "D":[self.params["I0"]*self.params["darkrate"]],
                                    "hard_course":[self.params["I0"]*self.params["hardrate"]],
                                    "deadly_course":[self.params["I0"]*self.params["deathrate"]]})

    def get_daily_numbers(self):
        steps_per_day = 1/self.params["dt"]
        data = pd.DataFrame({"S": [self.params['S0']], "E": [self.params['E0']], "I": [self.params['I0']], "R": [self.params['Re0']], "N": [
                            self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0']], "D": [self.params["I0"]*self.params["darkrate"]]})
        data = pd.DataFrame({"S": [self.params['S0']],
                             "E": [self.params['E0']],
                             "I": [self.params['I0']],
                             "R": [self.params['Re0']],
                             "N": [self.params['S0']+self.params['E0']+self.params['I0']+self.params['Re0']],
                             "D": [self.params["I0"]*self.params["darkrate"]],
                             "hard_course": [self.params["I0"]*self.params["darkrate"]*self.params["hardrate"]],
                             "deadly_course": [self.params["I0"]*self.params["darkrate"]*self.params["deathrate"]]})
        i = round(steps_per_day)
        while i < self.series.shape[0]:
            data = data.append(self.series.iloc[i, :], ignore_index=True)
            i = round(i + steps_per_day)
        return data

if __name__ == "__main__" :
    model = SEIRModel({
                    'beta': 0.27,  # The parameter controlling how often a susceptible-infected contact results in a new exposure.
                    'gamma':0.056,  # The rate an infected recovers and moves into the resistant phase.
                    'sigma': 50, # The rate at which an exposed person becomes infective.
                    'mu': 0,      # The natural mortality rate (this is unrelated to disease). This models a population of a constant size,
                    'nu': 0,      # Ich glaube Immunrate. Wie viele Leute von sich aus Immun sind gegen COVID19
                    'dt': 0.1,
                    'S0': 83e6,
                    'E0': 0,
                    'I0': 32.6,
                    'Re0': 0,
                    'darkrate': 0.10, # erstmal China studie # Quelle: Linton MN, Kobayashi T, Yang Y, Hayashi K, Akhmetzhanov RA, Jung S-m, et al. Incubation Period and Other Epidemiological Characteristics of 2019 Novel Coronavirus Infections with Right Truncation: A Statistical Analysis of Publicly Available Case Data. Journal of clinical medicine. 2020.
                    'hardrate': 0.154, # WHO studie:  Novel Coronavirus (2019-nCoV). (PDF; 0,9 MB) Situation Report – 18. WHO, 7. Februar 2020, abgerufen am 8. Februar 2020.
                    'deathrate': 0.034 # WHO :  Eröffnungsrede des WHO-Generaldirektors – Pressekonferenz zu COVID-19 – 3. März 2020. WHO, 3. März 2020, abgerufen am 6. März 2020 (englisch).
                    },
                    {'date_of_action':30,
                    'beta':0.6,
                    'gamma':0.2,
                    'sigma':0.5,
                    'mu':0,
                    'nu':0})

    prediction = model.compute(days=60,with_action=True)
    print(prediction)
