import numpy as np
import pandas as pd
from dataHandler import DataHandler
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
import os
from SEIRmodel import SEIRModel
class Visualizer:
    def __init__(self, dataHandler):
        dataHandler.loadData()
    def visualize(self, country):
        for item in ["confirmed", "deaths", "recovered"]:
            hover = HoverTool(tooltips=[
                ("Sepal length", "@sepal_length"),
                ("Sepal width", "@sepal_width"),
                ("Petal length", "@petal_length"),
                ("Species", "@species")
            ])
            p = figure(title="", plot_height=500, plot_width=500,
                   tools=[hover, "pan,reset,wheel_zoom"])

            p.xaxis.axis_label = 't/days'
            p.yaxis.axis_label = '# {} cases'.format(item)
            y_data = dataHandler.filterForCountry(country)[item][0]
            t=np.linspace(1, len(y_data), len(y_data))
            p.line(t, y_data, legend_label="blup", line_width=2)
            if not os.path.exists("docs/_includes/plots/{}/".format(country)):
                 os.makedirs("docs/_includes/plots/{}/".format(country))
            output_file('docs/_includes/plots/{}/{}_cases.html'.format(country, item))
            save(p)

#####***************


dataHandler = DataHandler()
Visualizer(dataHandler).visualize("Germany")
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
       'S0': 30,
       'E0': 0,
       'I0': 1,
       'Re0': 0})

prediction = model.compute(steps=150)
#pred = model.compute(steps=20)
print(model.get_daily_numbers())
