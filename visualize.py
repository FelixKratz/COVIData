import numpy as np
import pandas as pd
import os
from bokeh.io import output_file
from bokeh.embed import components
from bokeh.plotting import figure, show, save
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import reset_output
from bokeh.models import ColumnDataSource

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
    def visualize_tabs(self, country):
        self.ind_start_infection = np.argmax(dataHandler.filterForCountry(country)["confirmed"])
        pannels=[]    
        output_file('docs/_includes/plots/{}/all_cases.html'.format(country), title="CORINNA 17- Cases Germany")
        for item in ["confirmed", "deaths", "recovered"]:

            fig = figure(title="", plot_height=500, plot_width=500,
                       tools=["pan,reset,wheel_zoom"])

            fig.xaxis.axis_label = 't/days'
            fig.yaxis.axis_label = '# {} cases'.format(item)
            y_data = dataHandler.filterForCountry(country)[item]
            t = np.linspace(1, len(y_data), len(y_data))
            hist,edges=np.histogram(y_data,bins=len(t)) #numpy hist
            hist_df = pd.DataFrame({"cols": hist,
                                    "left": edges[:-1],
                                    "right": edges[1:]}) #dataframe hist for bokeh
            src = ColumnDataSource(hist_df)
            fig.vbar(x=t, bottom=0, top=y_data, color="Blue", width=0.99, legend_label="Daily")

            if not os.path.exists("docs/_includes/plots/{}/".format(country)):
                 os.makedirs("docs/_includes/plots/{}/".format(country))

            

            pannels.append(Panel(child=fig, title="{}".format(item)))
        tabs=Tabs(tabs=pannels)
        save(tabs)
        script,div=components(tabs)    
        with open('docs/_includes/plots/{}/all_cases.html'.format(country), 'w') as f:
            f.write(div)
            f.write(script)



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
            hist,edges=np.histogram(y_data,bins=len(t)) #numpy hist
            hist_df = pd.DataFrame({"cols": hist,
                                    "left": edges[:-1],
                                    "right": edges[1:]}) #dataframe hist for bokeh
            src = ColumnDataSource(hist_df)
            p.line(t, y_data, legend_label="blusdfp", line_width=2)                         
            p.vbar(x=t, bottom=0, top=y_data, color="Blue", width=0.99, legend_label="Daily")

            if not os.path.exists("docs/_includes/plots/{}/".format(country)):
                 os.makedirs("docs/_includes/plots/{}/".format(country))

            output_file(
                'docs/_includes/plots/{}/{}_cases.html'.format(country, item))

            save(p)
            reset_output()
    def visualize(self, country):
        self.visualize_simple(country)
        self.visualize_tabs(country)
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
