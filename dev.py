from dataHandler import DataHandler

dataHandler = DataHandler()
dataHandler.loadData()

#print(dataHandler.data['confirmed'].columns())
df = dataHandler.data['confirmed']
germany=df[df['Country/Region']=="Germany"]
