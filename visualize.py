import numpy as np
import pandas as pd
from dataHandler import DataHandler
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
import os
from SEIRmodel import SEIRModel
class Visualizer:
    def __init__(self, dataHandler, model, steps, death_rate):
        model.compute(steps)
        self.cases=model.get_daily_numbers()
        dataHandler.loadData()
        self.infected=self.cases["I"].to_numpy()
        self.removed=self.cases["R"]
        self.recovered=self.removed*(1-death_rate)
        self.deceased=self.removed*death_rate
        self.darkrate = model.params["darkrate"]
    def visualize(self, country):
        for item in ["confirmed", "deaths", "recovered"]:
            hover = HoverTool(tooltips=[
                ("Sepal length", "@sepal_length"),
                ("Sepal width", "@sepal_width"),
                ("Petal length", "@petal_length"),
                ("Species", "@species")
            ])
            print(self.darkrate)
            p = figure(title="", plot_height=500, plot_width=500,
                   tools=[hover, "pan,reset,wheel_zoom"])
            print(type(self.cases["R"]))
            print(len(self.infected))
            p.xaxis.axis_label = 't/days'
            p.yaxis.axis_label = '# {} cases'.format(item)
            y_data = dataHandler.filterForCountry(country)[item]


            ind=np.where(y_data>=1)


            t=np.linspace(1, len(y_data), len(y_data))
            p.line(t, y_data, legend_label="blup", line_width=2)
            if not os.path.exists("docs/_includes/plots/{}/".format(country)):
                 os.makedirs("docs/_includes/plots/{}/".format(country))
            output_file('docs/_includes/plots/{}/{}_cases.html'.format(country, item))
            save(p)

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
    'S0': 82000000,
    'E0': 0,
    'I0': 10,
    'Re0': 0,
    # Quelle: An der Heiden M, Buchholz U, Buda S. Estimation of influenza- and respiratory syncytial virus-attributable medically attended acute respiratory infections in Germany, 2010/11-2017/18. Influenza Other Respir Viruses. 2019.
    'darkrate': 0.05
})
Visualizer(dataHandler, model, steps=1000, death_rate=0.02).visualize("Germany")
