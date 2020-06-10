from connection import app

from flask import jsonify
from flask import request
import requests
from config import config
import json

class covid_api:

    @app.route('/api/<state>', methods=['GET'])
    def historical_data_by_state(state):
        response = requests.get(config.covid_api + state + "/daily.json")

        if (str(response.status_code) != "200") :
            return jsonify(
                {
                    "Error": str(response.status_code) + ": Server Error(Invalid request)"
                }
                )
        for item in response.content:
            print(type(response.content))
        data = json.loads(response.content)
        result = {}

        for i in range(0, len(data)):
            result[i] = data[i]

        return result

    @app.route('/api/<state>/<date>', methods=['GET'])
    def covid_data_by_date(state,date):
        response = requests.get(config.covid_api + state + "/"+date+".json")

        if (str(response.status_code) != "200") :
            return jsonify(
                {
                    "Error": str(response.status_code) + ": Server Error(Invalid request)"
                }
                )
        return json.loads(response.text)
    
    @app.route('/api/<state>/current', methods=['GET'])
    def covid_data_now(state):
        response = requests.get(config.covid_api + state + "/current.json")

        if (str(response.status_code) != "200") :
            return jsonify(
                {
                    "Error": str(response.status_code) + ": Server Error(Invalid request)"
                }
                )
        return json.loads(response.text)