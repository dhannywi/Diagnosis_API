from flask import Flask, request
import redis
import requests
import json
import csv
#import matplotlib.pyplot as plt
import os

app = Flask(__name__)


def get_redis_client(db_num: int):
    #redis_ip = os.environ.get('REDIS_IP')
    #if no redis_ip:
    #    raise Exception()
    #return redis.Redis(host='redis_ip', port=6379, db=db_num, decode_responses=True)
    return redis.Redis(host='redis-db', port=6379, db=db_num, decode_responses=True)

rd0 = get_redis_client(0)
rd1 = get_redis_client(1)


def get_method() -> dict:
    global rd0
    try:
        return json.loads(rd0.get('breast_cancer_cases'))
    except Exception as err:
        return f'Error. Data not loaded in\n', 404

@app.route('/data', methods = ['POST', 'GET', 'DELETE'])
def breast_cancer_data() -> dict:
    global rd0
    if request.method == 'POST':
        try:
            r = requests.get(url='https://raw.githubusercontent.com/dhannywi/Prognosis_API/main/wdbc.data.csv')
            data = {}
            data['breast_cancer_data'] = []
            csv_data = r.content.decode('utf-8')
            csv_reader = csv.DictReader(csv_data.splitlines())
            for row in csv_reader:
                data['breast_cancer_data'].append(dict(row))
            rd0.set('breast_cancer_cases', json.dumps(data['breast_cancer_data']))
        except Exception as err:
            return f'Error. Data not loaded in\n', 404
        return f'Data loaded in\n'

    elif request.method == 'GET':
        return get_method()

    elif request.method == 'DELETE':
        rd0.flushdb()
        return f'Data deleted\n'
                          
    else:
        return f'No available method selected. Methods available: POST, GET, DELETE\n', 404


@app.route('/data/id', methods = ['GET'])
def breast_cancer_id() -> dict:
    return f'test'


@app.route('/data/id/<id_num>', methods = ['GET'])
def id_data() -> dict:
    return f'test'





@app.route('/image', methods = ['GET'])
def create_imaget():
    return f'test'




@app.route('/help', methods = ['GET'])
def all_routes() -> str:
    return f'test'

    
if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
