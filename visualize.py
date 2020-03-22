import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
from bokeh.io import output_file
from bokeh.embed import components
from bokeh.plotting import figure, show, save
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import reset_output
from bokeh.models import ColumnDataSource, HoverTool

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



    def visualize_tabs(self, country):
        self.ind_start_infection = np.argmax(dataHandler.filterForCountry(country)["confirmed"])
        pannels=[]    
        output_file('docs/_includes/plots/{}/all_caseshtm.html'.format(country), title="CORINNA 17- Cases Germany")
        for item in ["confirmed", "deaths", "recovered"]:
            y_data = dataHandler.filterForCountry(country)[item]
            t = np.linspace(1, len(y_data), len(y_data))
            hist,edges=np.histogram(y_data,bins=len(t)) #numpy hist
            hist_df = pd.DataFrame({"cols": hist,
                                    "data": y_data,
                                    "date": [(datetime(2020,1,22)+timedelta(days=time)).strftime("%d.%m.%Y") for time in t],
                                    "time": t,
                                    "left": edges[:-1],
                                    "right": edges[1:]}) #dataframe hist for bokeh
            src = ColumnDataSource(hist_df)
        

            Tooltips = [
                ('Cases', '@data'),
                ('Date', '@date'),
            ]
            fig = figure(title="", plot_height=500, plot_width=500,
                         tools=["pan,reset,wheel_zoom, hover, tap"], tooltips=Tooltips)
            fig.xaxis.axis_label = 't/days'
            fig.yaxis.axis_label = '# {} cases'.format(item)
            fig.xaxis.major_label_overrides = dict(zip(hist_df.time, hist_df.date))
            fig.vbar(x="time", bottom=0, top="data", color="Blue", width=0.99, legend_label="cases per day", line_width=0.1,source=src)
            
            
            if not os.path.exists("docs/_includes/plots/{}/".format(country)):
                 os.makedirs("docs/_includes/plots/{}/".format(country))
            
            pannels.append(Panel(child=fig, title="{}".format(item))) #adds each pannel to tabs
        tabs=Tabs(tabs=pannels)
        save(tabs)
        




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

    def visualize_stacked(self, country):
        output_file('docs/_includes/plots/{}/stacked.html'.format(country),
                    title="COREA- Cases Germany")
        diff_types = ["Confirmed", "Deaths", "Recovered"]
        colors = ["#c9d9d3", "#718dbf", "#e84d60"]
        y_data = dataHandler.filterForCountry(country)
        t = np.linspace(1, len(y_data["recovered"]), len(y_data["recovered"]))
        
        data={
            'time':t,
            "date": [(datetime(2020, 1, 22)+timedelta(days=time)).strftime("%d.%m.%Y") for time in t],
            'Confirmed':y_data["confirmed"],
            'Deaths':  y_data["deaths"],
            'Recovered':  y_data["recovered"]
                }
       
        p = figure(x_range=data["date"], title="Stacked Cases COVID-19 {}".format(country), plot_height=500, plot_width=500,
                   tools=["pan,reset,wheel_zoom, tap"])


        renderers=p.vbar_stack(diff_types, x='time', width=0.9, color=colors, source=data,
             legend_label=diff_types)
        for renderer in renderers:
            case_type=renderer.name
            hover=HoverTool(tooltips=[
                ("%s total" % case_type, "@%s" % case_type),
                ('Date', '@date'),
            ], renderers=[renderer])
            p.add_tools(hover)
        save(p)
        reset_output()
    def visualize(self, country):
        self.visualize_simple(country)
        self.visualize_tabs(country)
        self.visualize_stacked(country)
        self.__rm_doctype(country)
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
Visualizer(dataHandler, model, steps=150, death_rate=0.02).visualize("Germany")
