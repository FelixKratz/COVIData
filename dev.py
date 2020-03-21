from dataHandler import DataHandler

dataHandler = DataHandler()
dataHandler.loadData()
tmp=dataHandler.filterForCountry("Germany")["confirmed"]
print(tmp)
