from dataHandler import DataHandler

dataHandler = DataHandler()
dataHandler.loadData()

germanData = dataHandler.filterForCountry("Germany")
print(germanData)
