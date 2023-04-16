from flask import Flask, request
import redis
import requests
import json
import csv
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

r = requests.get('https://raw.githubusercontent.com/dhannywi/Prognosis_API/main/wdbc.data.csv')
def make_json():
    data = {}
    

@app.route('/data', methods = ['POST', 'GET', 'DELETE'])
def breast_cancer_data() -> dict:
    if request.method == 'POST':
        r = requests.get(url='https://github.com/dhannywi/Prognosis_API/blob/main/wdbc.data.csv')
        df = pd.read_csv(r)
        df.to_json (r'/csvtojsontest.json')



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
