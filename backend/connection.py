"""
Author: Sudhansu Shrestha
Date: 5/30/2020

Restful API

Comments: I need to find a way to automate package installation, docker might come in handy

To RUN: 

Install packages using:
pip install everything in requirements.txt

Then in cmd:

export FLASK_APP=connection.py
flask run


"""
from flask import Flask
from flask_pymongo import pymongo
from config import config
import folium
from folium.plugins import TimestampedGeoJson
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['MONGO_DBNAME'] = config.db_name
app.config['MONGO_URI'] = config.connection_url
import read, covid_api, create, update, delete
# import create

# import update
# import delete

@app.route('/')
def number_cases():
    latitude = 37.0902
    longitude = -95.7129
    covid_map = folium.Map(location=[latitude, longitude], zoom_start=5)
    state_boundaries = 'http://data-lakecountyil.opendata.arcgis.com/datasets/3e0c1eb04e5c48b3be9040b0589d3ccf_8.geojson'
    data = "https://coronadatascraper.com/data.csv"
    folium.GeoJson(state_boundaries).add_to(covid_map)
    covid_data = pd.read_csv(data)
    covid_data.head()

    folium.Choropleth(
        geo_data = state_boundaries,
        name = 'choropleth',
        data = covid_data,
        columns = ['state', 'cases'],
        key_on = 'feature.properties.NAME',
        fill_color = 'YlOrRd',
        fill_opacity = 0.9,
        line_opacity = 0.5,
        legend_name = "COVID cases"
    ).add_to(covid_map)

    folium.LayerControl().add_to(covid_map)
    return covid_map._repr_html_()

class mongo_connection:

    @staticmethod
    def connect():
        mongo = pymongo(app)
        return mongo
    
    
