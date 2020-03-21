import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
import os
from bokeh.charts import Histogram
from bokeh.charts import defaults, vplot, hplot, show, output_file
from dataHandler import DataHandler
from SEIRmodel import SEIRModel
class Visualizer:
    def __init__(self, dataHandler, model, steps, death_rate):
        model.compute(steps)
        self.cases=model.get_daily_numbers()
        dataHandler.loadData()
        self.darkrate =model.params["darkrate"]
        self.infected=self.cases["I"].to_numpy()*self.darkrate #nur 5% der infizierten werden registriert
        self.removed=self.cases["R"]*self.darkrate #nicht alle recorvered werden registriert evtl mehr als darkrate infected?
        self.recovered=self.removed*(1-death_rate) 
        self.deceased=self.removed*death_rate
        



    def visualize_simple(self, country):
        self.ind_start_infection = np.argmax(
            dataHandler.filterForCountry(country)["confirmed"])
        for item in ["confirmed", "deaths", "recovered"]:

            p = figure(title="", plot_height=500, plot_width=500,
                       tools=["pan,reset,wheel_zoom"])

            p.xaxis.axis_label = 't/days'
            p.yaxis.axis_label = '# {} cases'.format(item)
            y_data = dataHandler.filterForCountry(country)[item]
            t = np.linspace(1, len(y_data), len(y_data))
            p.line(t, y_data, legend_label="blusdfp", line_width=2)

            if not os.path.exists("docs/_includes/plots/{}/".format(country)):
                 os.makedirs("docs/_includes/plots/{}/".format(country))

            output_file(
                'docs/_includes/plots/{}/{}_cases.html'.format(country, item))

            save(p)
    def visualize(self, country):
        self.visualize_simple(country)
#####***************


dataHandler = DataHandler()

model = SEIRModel({
    # The parameter controlling how often a susceptible-infected contact results in a new exposure.
    'beta': 0.9,
    # The rate an infected recovers and moves into the resistant phase.
    'gamma': 0.2,
    # The rate at which an exposed person becomes infective.
    'sigma': 0.5,
    # The natural mortality rate (this is unrelated to disease). This models a population of a constant size,
    'mu': 0,
    'nu': 0,      # Ich glaube Immunrate. Wie viele Leute von sich aus Immun sind gegen COVID19
    'dt': 0.1,
    'S0': 83e6,
    'E0': 0,
    'I0': 1,
    'Re0': 0,
    # erstmal China studie # Quelle: Linton MN, Kobayashi T, Yang Y, Hayashi K, Akhmetzhanov RA, Jung S-m, et al. Incubation Period and Other Epidemiological Characteristics of 2019 Novel Coronavirus Infections with Right Truncation: A Statistical Analysis of Publicly Available Case Data. Journal of clinical medicine. 2020.
    'darkrate': 0.05,
    # WHO studie:  Novel Coronavirus (2019-nCoV). (PDF; 0,9 MB) Situation Report – 18. WHO, 7. Februar 2020, abgerufen am 8. Februar 2020.
    'hardrate': 0.154,
    # WHO :  Eröffnungsrede des WHO-Generaldirektors – Pressekonferenz zu COVID-19 – 3. März 2020. WHO, 3. März 2020, abgerufen am 6. März 2020 (englisch).
    'deathrate': 0.034
})
Visualizer(dataHandler, model, steps=100, death_rate=0.02).visualize("Germany")
