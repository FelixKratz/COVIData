import numpy as np
import pandas as pd
from dataHandler import DataHandler
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
import os
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
            if not os.path.exists("docs/plots/{}/".format(country)):
                 os.makedirs("docs/plots/{}/".format(country))
            output_file('docs/plots/{}/{}_cases.html'.format(country, item))
            save(p)

#####***************


dataHandler = DataHandler()
Visualizer(dataHandler).visualize("Germany")
