import numpy as np
import pandas as pd

class DataHandler:
    def __init__(self):
        self.dataURLs = {'confirmed' : "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv",
                         'deaths' : "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv",
                         'recovered' : "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv" }
        self.data = {'confirmed': [], 'deaths': [], 'recovered': []}

    def loadData(self):
        self.data['confirmed'] = pd.read_csv(self.dataURLs['confirmed'])
        self.data['deaths'] = pd.read_csv(self.dataURLs['deaths'])
        self.data['recovered'] = pd.read_csv(self.dataURLs['recovered'])
