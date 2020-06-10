from connection import app

from flask import jsonify
from flask import request

@app.route('/readValue', methods=['GET'])
def read_value():
  return jsonify({'result' : 'FOUND'})
  
