import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


data2020 = pd.read_csv(
    os.path.join(
        "data", "waqi-covid19-airqualitydata-2020.csv"), 
        skiprows = 4, parse_dates=["Date"]
    )

data2020 = data2020[data2020.Country == "US"].set_index("Date")

data2019 = pd.read_csv(
    os.path.join(
        "data", "waqi-covid19-airqualitydata-2019Q1.csv"), 
        skiprows = 4, parse_dates=["Date"])

data2019 = data2019.append(
    pd.read_csv(
        os.path.join("data", 
            "waqi-covid19-airqualitydata-2019Q2.csv"
        ),  skiprows = 4, parse_dates=["Date"])
    )

data2019 = data2019[data2019.Country == "US"].set_index("Date")



covidData = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")

# when did the county/city pass 100 cumulative cases? 

citiesWithAQI = set(data2020.City.unique())
citiesWithCaseNums = set(covidData.county.unique())
cities = citiesWithAQI.intersection(citiesWithCaseNums)

cities.add("New York City")
cities.add("District of Columbia")

remainingCities = cities.copy()
startDates = {}

for city in cities:
    
    cityData = covidData[covidData.county == city]
    row = np.searchsorted(cityData.cases, 25)
    try:
        startDates[city] = cityData.iloc[row, 0]
    except IndexError as e:
        print("Bad data for " + city)
        remainingCities.remove(city)

nyc = {'Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'The Bronx'}



for city, start in startDates.items():

    if city=="New York City":
        cityMask2020 = data2020.apply(lambda row: row.City in nyc, axis = 1) 
        cityMask2019 = data2019.apply(lambda row: row.City in nyc, axis = 1) 
    else:
        cityMask2020 = (data2020.City == city)
        cityMask2019 = (data2019.City == city)

    cityMask2020 = cityMask2020 & ((data2020["Specie"] == "no2") | (data2020["Specie"] == "pm25"))
    cityMask2019 = cityMask2019 & ((data2019["Specie"] == "no2") | (data2019["Specie"] == "pm25"))

    data2020subset = data2020.loc[(data2020.index >= start) &
        cityMask2020, ["Specie", "median"]]
    data2020subset['Days since start'] = pd.Series(data2020subset.index - 
        pd.to_datetime(start)).dt.days.values
    data2020subset = data2020subset.set_index(
        ["Days since start", "Specie"])
     
    data2019subset = data2019.loc[(data2019.index >= pd.to_datetime(start) - pd.Timedelta(1, unit='y')) & 
        cityMask2019, ["Specie", "median"]]
    data2019subset["Days since start"] = pd.Series(data2019subset.index -
        (pd.to_datetime(start) - pd.Timedelta(1, unit='y'))).dt.days.values
    data2019subset = data2019subset.set_index(
        ["Days since start", "Specie"])
    
    # del data2020subset["Date"]
    # del data2019subset["Date"]
    

    if city=="New York City":
        data2020subset = data2020subset.groupby(["Days since start", "Specie"]).mean()
        data2019subset = data2019subset.groupby(["Days since start", "Specie"]).mean()


    try:
        data2020subset = data2020subset.unstack()
        data2019subset = data2019subset.unstack()

        combinedData = data2019subset.merge(
        data2020subset, suffixes=("_2019", "_2020"), on = "Days since start")

        combinedData["Relative NO2 Levels"] = combinedData["median_2020"]["no2"] / combinedData["median_2019"]["no2"]
        combinedData["Relative PM2.5 Levels"] = combinedData["median_2020"]["pm25"] / combinedData["median_2019"]["pm25"]
        
        
        fig, ax = plt.subplots(figsize=(8, 5))

        plt.plot(combinedData[["Relative NO2 Levels", 
            "Relative PM2.5 Levels"]].rolling(7).mean())
        
        ax.legend(loc='best')
        ax.set_xlabel("Days since start")
        ax.set_ylabel("Relative pollution")
        plt.savefig(os.path.join("output", "Relative pollution for" + f" {city} starting from {start}"))
        plt.clf()
    except KeyError as e:
        print(e)
   

# on = "Date", suffix=["_2020", "_2019"]
 
