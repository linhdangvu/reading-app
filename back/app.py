from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json
# import logging

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
    #print(response_API.status_code)
    data = response_API.text
    parse_json = json.loads(data)
    active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
    print("Active cases in South Andaman:", active_case)    
    return "Hello world"


if __name__ == '__main__':
    app.run()