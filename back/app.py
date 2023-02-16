from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# try to get only 10 book
@app.route('/getbooks', methods=['GET'])
def getBooks():
    response_API = requests.get('https://gutendex.com/books/')
    #print(response_API.status_code)
    data = response_API.text
    parse_json = json.loads(data)
    logging.info("Get data ok")
    print(len(parse_json['results']))
    return jsonify(parse_json['results'])


if __name__ == '__main__':
    app.run()