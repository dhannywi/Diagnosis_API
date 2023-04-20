from flask import Flask, request, send_file
import redis
import requests
import json
import csv
import matplotlib.pyplot as plt
import os
import yaml

app = Flask(__name__)

#redis_ip = os.environ.get('REDIS_IP')
#if not redis_ip:
#    raise Exception()
rd0 = redis.Redis(host='redis-db', port=6379, db=0, decode_responses=True)
rd1 = redis.Redis(host='redis-db', port=6379, db=1)


def get_method() -> dict:
    global rd0
    try:
        data = []
        for item in rd0.keys():
            data.append(json.loads(rd0.get(item)))
        return data
    except Exception as err:
        return f'Error. Data not loaded in\n', 404

def m_cases() -> int:
    global rd0
    try:
        val_m = 0
        for key in rd0.keys():
            m_or_b = json.loads(rd0.get(key))['Diagnosis']
            if m_or_b == 'M':
                val_m += 1
        return val_m
    except Exception as err:
        return f'Error. Data not loaded in\n', 404

def b_cases() -> int:
    global rd0
    try:
        val_b = 0
        for key in rd0.keys():
            m_or_b = json.loads(rd0.get(key))['Diagnosis']
            if m_or_b == 'B':
                val_b += 1
        return val_b
    except Exception as err:
        return f'Error. Data not loaded in\n', 404
    
@app.route('/data', methods = ['POST', 'GET', 'DELETE'])
def breast_cancer_data() -> dict:
    global rd0
    if request.method == 'POST':
        try:
            r = requests.get(url='https://raw.githubusercontent.com/dhannywi/Prognosis_API/main/wdbc.data.csv')
            csv_data = r.content.decode('utf-8')
            csv_reader = csv.DictReader(csv_data.splitlines())
            data = {}
            for row in csv_reader:
                id_num = row.get('ID Number')
                rd0.set(id_num, json.dumps(row))
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


@app.route('/id', methods = ['GET'])
def cancer_case_id() -> dict:
    if rd0.keys() == 0:
        return f'Error. Data not loaded in\n', 404
    return rd0.keys()


@app.route('/id/<id_num>', methods = ['GET'])
def id_data(id_num: int) -> dict:
    if rd0.keys() == 0:
        return f'Error. Data not loaded in\n', 404
    try:
        return json.loads(rd0.get(id_num))
    except Exception as err:
        return f'Error. ID {id_num} not found in database\n', 404


@app.route('/outcome', methods = ['GET'])
def get_cases() -> dict:
    try:
        m_list = []
        b_list = []
        for key in rd0.keys():
            m_or_b = json.loads(rd0.get(key))['Diagnosis']
            if m_or_b == 'M':
                m_list.append(key)
            elif m_or_b == 'B':
                b_list.append(key)
        val_m = m_cases()
        val_b = b_cases()
        cases = {"Malignant": {"Total cases": val_m, "IDs": m_list}, "Benign": {"Total cases": val_b, "IDs": b_list}}
        return cases
    except Exception as err:
        return f'Error. Data not loaded in\n', 404


@app.route('/image', methods = ['POST', 'GET', 'DELETE'])
def image():
    global rd0, rd1
    if request.method == 'POST':
        graph_data = {}
        if len(rd0.keys()) == 0:
            return f'Data not loaded into database\n', 404
        val_m = m_cases()
        val_b = b_cases()
        graph_data = {'Malignant': val_m, 'Benign': val_b}
        diagnosis = list(graph_data.keys())
        num_diagnosis = list(graph_data.values())
        plt.bar(diagnosis, num_diagnosis, color = 'maroon', width = .4)
        plt.xlabel("Prognosis")
        plt.ylabel("Number of Cases")
        plt.title("Breast Cancer Cases Prognosis")
        plt.savefig('./cancer_prognosis.png')
        image_data = open('./cancer_prognosis.png', 'rb').read()
        rd1.set('image', image_data)
        return f'Graph successfully saved\n'

    elif request.method == 'GET':
        if len(rd0.keys()) == 0:
            return f'Data not loaded into database\n', 404
        try:
            image_data = rd1.get('image')
            if image_data is None:
                return f'Error. No image found\n', 404
            with open('./cancer_prognosis.png', 'wb') as image_file:
                image_file.write(image_data)
            return send_file('./cancer_prognosis.png', mimetype = 'image/png', as_attachment = True)
        except Exception as err:
            return f'Error. Unable to fetch image\n', 404

    elif request.method == 'DELETE':
        try:
            rd1.flushdb()
            return f'Image deleted\n'
        except Exception as err:
            return f'Unable to delete image\n', 404

    else:
        return f'No available method selected. Methods available: POST, GET, DELETE\n', 404


@app.route('/help', methods = ['GET'])
def all_routes() -> str:
    return '''\n Usage: curl 'localhost:5000[OPTIONS]'\n
    Options:\n
    1. /data
    '''

    
if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
