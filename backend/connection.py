"""
Author: Sudhansu Shrestha
Date: 5/30/2020

Restful API

Comments: I need to find a way to automate package installation, docker might come in handy

To RUN: 

Install packages using:
pip install < requirements.txt 

Then in cmd:

export FLASK_APP=connection.py
flask run

"""
from flask import Flask
from flask_pymongo import pymongo
from config import config

app = Flask(__name__)
app.config['MONGO_DBNAME'] = config.db_name
app.config['MONGO_URI'] = config.connection_url
import read
# import create

# import update
# import delete

@app.route('/')
def hello_world():
    return 'Hello, World!'

class mongo_connection:

    @staticmethod
    def connect():
        mongo = pymongo(app)
        return mongo
    
    
