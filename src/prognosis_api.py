from flask import Flask, request
import redis
import requests
import json
import csv
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/data', methods = ['POST', 'GET', 'DELETE'])
def breast_cancer_data() -> dict:
    if request.method == 'POST':
        r = requests.get(url='https://raw.githubusercontent.com/dhannywi/Prognosis_API/main/wdbc.data.csv')
        data = {}
        data['breast_cancer_data'] = []
        csv_data = r.content.decode('utf-8')
        csv_reader = csv.DictReader(csv_data.splitlines())
        #json_data = json.dumps([row for row in csv_reader], ensure_ascii=False)
        for row in csv_reader:
            data['breast_cancer_data'].append(dict(row))
        return f'Data loaded in\n'
    elif request.method == 'GET':



    elif request.method == 'DELETE':
            


    else:
        return f'No available method selected. Methods available: POST, GET, DELETE\n', 404




@app.route('/data/id', methods = ['GET'])
def breast_cancer_id() -> dict:
    


@app.route('/data/id/<id_num>', methods = ['GET'])
def id_data() -> dict:






@app.route('/image', methods = ['GET'])
def create_imaget():





@app.route('/help', methods = ['GET'])
def all_routes() -> str:
    

    
if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
