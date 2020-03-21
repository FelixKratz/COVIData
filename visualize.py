import numpy as np

from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool


def lin(x):
    return 3*x


x = np.linspace(0, 10)
hover = HoverTool(tooltips=[
    ("Sepal length", "@sepal_length"),
    ("Sepal width", "@sepal_width"),
    ("Petal length", "@petal_length"),
    ("Species", "@species")
])

p = figure(title="lin", plot_height=500, plot_width=500,
           tools=[hover, "pan,reset,wheel_zoom"])

p.xaxis.axis_label = 'x'
p.yaxis.axis_label = 'y'

p.line(x, lin(x), legend_label="blup", line_width=2)

output_file('docs/testplot.html')

show(p)
