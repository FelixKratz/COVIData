import numpy as np
import pandas as pd
import os
import math
from datetime import datetime, timedelta

#bokeh
from bokeh.io import output_file
from bokeh.embed import components
from bokeh.plotting import figure, show, save, ColumnDataSource, reset_output
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import  HoverTool, CustomJS, Slider

from dataHandler import DataHandler
from SEIRmodel import SEIRModel

class Visualizer:
    def __init__(self, dataHandler, model, steps, death_rate):
        self.cases = model.compute(steps)
        print(self.cases)
        dataHandler.loadData()
        self.darkrate =model.params["darkrate"]
        self.detected=self.cases["D"] #nur 5% der infizierten werden registriert
        print(self.detected)
        self.infected=self.cases["I"]
        self.deceased=self.cases["deadly_course"]
        self.recovered=self.cases["R"]- self.deceased

    ##dirty helper:
    def __rm_doctype(self,country):
        #folgender Code ist so dirty, da hilft noch nicht mal 30 sec. Händewaschen... AAber er entfernt immer den Doctype html
        path = os.getcwd()+"/docs/_includes/plots/{}/".format(country)
        htmlfiles = [os.path.join(path, file) for file in os.listdir(path) if file.endswith((".html", ".htm"))]
        for file in htmlfiles:
            with open(file) as f_in:
                w_o_doctype = f_in.read().splitlines(True)
            with open(file, "w") as f_out:
                f_out.writelines(w_o_doctype[5:])
    def visualize_model_data(self, country):
        self.ind_start_infection = np.argmax(
            dataHandler.filterForCountry(country)["confirmed"] >= 1)
        output_file('docs/_includes/plots/{}/model_data.html'.format(country), title="CORINNA 17- Cases Germany")
        diff_types = ["Confirmed", "Deaths", "Recovered"]
        colors = ["#c9d9d3", "#718dbf", "#e84d60"]
        y_data = dataHandler.filterForCountry(
            country)
        t = np.linspace(1, len(y_data["recovered"][self.ind_start_infection:]), len(
            y_data["recovered"][self.ind_start_infection:]))

        data={
            'time':t,
            "date": [(datetime(2020, 1, 22)+timedelta(days=time)).strftime("%d.%m.%Y") for time in t],
            'Confirmed': y_data["confirmed"][self.ind_start_infection:],
            'Deaths':  y_data["deaths"][self.ind_start_infection:],
            'Recovered':  y_data["recovered"][self.ind_start_infection:]
                }

        p = figure(x_range=data["date"], title="COVID-19-Cases {}. Including SEIR-Model".format(country), plot_height=500, plot_width=1000,
                   tools=["pan,reset,wheel_zoom, tap"])
        p.xaxis.major_label_orientation = math.pi/3
        p.line(t, self.detected[:len(t)], name="SEIR-Model: Detected cases")
        renderers=p.vbar_stack(diff_types, x='time', width=0.9, color=colors, source=data,
             name=diff_types)
        for renderer in renderers:
            case_type=renderer.name
            hover=HoverTool(tooltips=[
                ("%s total" % case_type, "@%s" % case_type),
                ('Date', '@date'),
            ], renderers=[renderer])
            p.add_tools(hover)
        print(type(list(model.params.keys())))
        df = pd.DataFrame({"Parameter":list(model.params.keys()), "value":list(model.params.values())})
        table=df.to_html()
        if not os.path.exists("docs/_includes/table/{}/".format(country)):
                     os.makedirs("docs/_includes/table/{}/".format(country))
        with open("docs/_includes/table/{}/model_data.html".format(country), "w") as f:
            f.write(table)
        save(p)
        reset_output()

    def visualilze_model(self):
        country="Germany"
        model1 = SEIRModel({
                        'beta': 0.6,
                        'gamma': 0.2,
                        'sigma': 0.5,
                        'mu': 0,
                        'nu': 0,
                        'dt': 0.1,
                        'S0': 83e6,
                        'E0': 0,
                        'I0': 1,
                        'Re0': 0,
                        'darkrate': 0.05,
                        'hardrate': 0.154,
                        'deathrate': 0.034
                        },[{'date_of_action':80,
                        'beta':0.6,
                        'gamma':0.2,
                        'sigma':0.5,
                        'mu':0,
                        'nu':0}])
        model2 = SEIRModel({
                        'beta': 0.6,
                        'gamma': 0.2,
                        'sigma': 0.5,
                        'mu': 0,
                        'nu': 0,
                        'dt': 0.1,
                        'S0': 83e6,
                        'E0': 0,
                        'I0': 1,
                        'Re0': 0,
                        'darkrate': 0.05,
                        'hardrate': 0.154,
                        'deathrate': 0.034
                        },[{'date_of_action':80,
                        'beta':0.3,
                        'gamma':0.2,
                        'sigma':0.5,
                        'mu':0,
                        'nu':0}])
        model3 = SEIRModel({
                        'beta': 0.6,
                        'gamma': 0.2,
                        'sigma': 0.5,
                        'mu': 0,
                        'nu': 0,
                        'dt': 0.1,
                        'S0': 83e6,
                        'E0': 0,
                        'I0': 1,
                        'Re0': 0,
                        'darkrate': 0.05,
                        'hardrate': 0.154,
                        'deathrate': 0.034
                        },[{'date_of_action':80,
                        'beta':0.8,
                        'gamma':0.2,
                        'sigma':0.5,
                        'mu':0,
                        'nu':0}])
        pred1 = model1.compute(days=200,with_action=True)
        pred2 = model2.compute(days=200,with_action=True)
        pred3 = model3.compute(days=200,with_action=True)

        colors = ["#c9d9d3", "#718dbf", "#e84d60"]

        output_file('docs/_includes/plots/{}/model.html'.format(country),
                    title="COREA- Cases Germany")

        t = np.linspace(1, 200, 200)

        p = figure(title="Effekt ", plot_height=500, plot_width=1000,
                   tools=["pan,reset,wheel_zoom, tap"])

        p.xaxis.major_label_orientation = math.pi/3
        p.xaxis.axis_label = 't/days'
        p.yaxis.axis_label = '# detected cases'
        p.line(t, pred1['hard_course'], name="without action", line_width=2, color=colors[0])
        p.line(t, pred2['hard_course'], name="positive action", line_width=2,color=colors[1])
        p.line(t, pred3['hard_course'], name="negative action", line_width=2,color=colors[2])
        save(p)
        reset_output()


    def visualize_interactive(self, country):
        x = np.linspace(0, 10, 500)
        y = np.sin(x)
        source = ColumnDataSource(data=dict(x=x, y=y))
        plot = figure(y_range=(-10, 10), plot_width=400, plot_height=400)
        plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
        slider = Slider(start=0.1, end=10, value=1, step=.1, title="Amplitude")
        callback = CustomJS(args=dict(source=source, amp=slider),
                    code="""
                    const data = source.data;
                    const A = amp.value;
                    const x = data['x']
                    const y = data['y']
                    for (var i = 0; i < x.length; i++) {
                        y[i] = A*Math.sin(x[i]);
                    }
                    source.change.emit();
        """)

        slider.js_on_change('value', callback)

        layout = row(
        plot,
        column(slider),
        )
        output_file('docs/_includes/plots/{}/slider.html'.format(country) , title="slider test")
        save(layout)
    def visualize_tabs(self, country):
        self.ind_start_infection = np.argmax(dataHandler.filterForCountry(country)["confirmed"]>=1)
        panels=[]
        scales=[]
        output_file('docs/_includes/plots/{}/all_caseshtm.html'.format(country), title="CORINNA 17- Cases Germany")
        for axis_type in ["linear", "log"]:

            for item in ["confirmed", "deaths", "recovered"]:
                y_data = dataHandler.filterForCountry(country)[item][self.ind_start_infection:]
                t = np.linspace(1, len(y_data), len(y_data))
                hist,edges=np.histogram(y_data,bins=len(t)) #numpy hist
                src ={"cols": hist,
                                        "data": y_data,
                                        "date": [(datetime(2020,1,22)+timedelta(days=time)).strftime("%d.%m.%Y") for time in t],
                                        "time": t,
                                        "left": edges[:-1],
                                        "right": edges[1:]} #dataframe hist for bokeh


                Tooltips = [
                    ('Cases', '@data'),
                    ('Date', '@date'),
                ]
                fig = figure(y_axis_type=axis_type,x_range=src["date"], title="", plot_height=500, plot_width=1000,
                             tools=["pan,reset,wheel_zoom, hover, tap"], tooltips=Tooltips)
                fig.xaxis.axis_label = 't/days'
                fig.yaxis.axis_label = '# {} cases'.format(item)
                fig.xaxis.major_label_orientation = math.pi/3

                #fig.xaxis.major_label_overrides = dict(zip(hist_df.time, hist_df.date))
                fig.vbar(x="time", bottom=0.01, top="data", color="Blue", width=0.99, name="cases per day", line_width=0.1,source=src)


                if not os.path.exists("docs/_includes/plots/{}/".format(country)):
                     os.makedirs("docs/_includes/plots/{}/".format(country))

                panels.append(Panel(child=fig, title="{}-{}".format(item, axis_type))) #adds each pannel to tabs
        tabs = Tabs(tabs=panels)
        save(tabs)




    def visualize_simple(self, country):
        self.ind_start_infection = np.argmax(
            dataHandler.filterForCountry(country)["confirmed"])
        for item in ["confirmed", "deaths", "recovered"]:

            p = figure(title="", plot_height=500, plot_width=1000,
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
            hist=p.vbar(x=t, bottom=1, top=y_data, color="Blue", width=0.99, name="Daily")
            hist.level="underlay"
            line=p.line(t, y_data, name="blusdfp", line_width=2)
            line.level="overlay"
            if not os.path.exists("docs/_includes/plots/{}/".format(country)):
                 os.makedirs("docs/_includes/plots/{}/".format(country))

            output_file(
                'docs/_includes/plots/{}/{}_cases.html'.format(country, item))

            save(p)
            reset_output()

    def visualize_stacked(self, country):
        self.ind_start_infection = np.argmax(
            dataHandler.filterForCountry(country)["confirmed"] >= 1)
        output_file('docs/_includes/plots/{}/stacked.html'.format(country),
                    title="COREA- Cases Germany")
        diff_types = ["Confirmed", "Deaths", "Recovered"]
        colors = ["#c9d9d3", "#718dbf", "#e84d60"]
        y_data = dataHandler.filterForCountry(
            country)
        t = np.linspace(1, len(y_data["recovered"][self.ind_start_infection:]), len(
            y_data["recovered"][self.ind_start_infection:]))

        data={
            'time':t,
            "date": [(datetime(2020, 1, 22)+timedelta(days=time)).strftime("%d.%m.%Y") for time in t],
            'Confirmed': y_data["confirmed"][self.ind_start_infection:],
            'Deaths':  y_data["deaths"][self.ind_start_infection:],
            'Recovered':  y_data["recovered"][self.ind_start_infection:]
                }

        p = figure(x_range=data["date"], title="Stacked Cases COVID-19 {}".format(country), plot_height=500, plot_width=1000,
                   tools=["pan,reset,wheel_zoom, tap"])

        p.xaxis.major_label_orientation = math.pi/3
        renderers=p.vbar_stack(diff_types, x='time', width=0.9, color=colors, source=data,
             name=diff_types)
        for renderer in renderers:
            case_type=renderer.name
            hover=HoverTool(tooltips=[
                ("%s total" % case_type, "@%s" % case_type),
                ('Date', '@date'),
            ], renderers=[renderer])
            p.add_tools(hover)
        save(p)
        reset_output()
    def visualize_longterm(self, country):
        self.ind_start_infection = np.argmax(
            dataHandler.filterForCountry(country)["confirmed"] >= 1)
        output_file('docs/_includes/plots/{}/model_longterm.html'.format(country), title="Covid19-Cases Germany")
        diff_types = ["Confirmed", "Deaths", "Recovered"]
        colors = ["#c9d9d3", "#718dbf", "#e84d60"]
        y_data = dataHandler.filterForCountry(country)
        t_data = np.linspace(1, len(y_data["recovered"][self.ind_start_infection:]), len(
            y_data["recovered"][self.ind_start_infection:]))
        t_model=np.linspace(30,len(self.detected) - 29, len(self.detected) - 29)
        data={
            'time':t_model,
            "date": [(datetime(2020, 1, 22)+timedelta(days=time)).strftime("%d.%m.%Y") for time in t_model],
            'Confirmed': np.append(y_data["confirmed"][self.ind_start_infection:],([0]*(len(t_model)-len(t_data)))),
            'Deaths':  np.append(y_data["deaths"][self.ind_start_infection:],([0]*(len(t_model)-len(t_data)))),
            'Recovered':  np.append(y_data["recovered"][self.ind_start_infection:],([0]*(len(t_model)-len(t_data))))
                }
        print(data["time"], data["Deaths"])
        p = figure(x_range=data["date"], title="COVID-19-Cases {}. Including SEIR-Model".format(country), plot_height=500, plot_width=1000,
                   tools=["pan,reset,wheel_zoom, tap"])
        p.xaxis.major_label_orientation = math.pi/3
        p.line(t_model, self.detected, name="SEIR-Model")
        renderers=p.vbar_stack(diff_types, x='time', width=0.9, color=colors, source=data,
             name=diff_types)
        for renderer in renderers:
            case_type=renderer.name
            hover=HoverTool(tooltips=[
                ("%s total" % case_type, "@%s" % case_type),
                ('Date', '@date'),
            ], renderers=[renderer])
            p.add_tools(hover)
            p.legend.click_policy = 'mute'
        save(p)
        reset_output()

    def visualize(self, country):
        self.visualize_simple(country)
        self.visualize_tabs(country)
        self.visualize_stacked(country)
        self.visualize_interactive(country)
        self.visualize_model_data(country)
        self.visualilze_model()
        self.visualize_longterm(country)

        self.__rm_doctype(country)
#####***************


dataHandler = DataHandler()

model = SEIRModel({'beta': 642.3430438150659, 'gamma': 3.5462661166540026, 'sigma': 0.0016878787803937588, 'mu': 0, 'nu': 0, 'dt': 0.1, 'S0': 83000000.0, 'E0': 0, 'I0': 249.0634121560787, 'Re0': 0, 'darkrate': 0.05, 'hardrate': 0.154, 'deathrate': 0.034}
)
Visualizer(dataHandler, model, steps=100, death_rate=0.02).visualize("Germany")
