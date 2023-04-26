from flask import Flask, request, send_file
import redis
import requests
import json
import csv
import matplotlib.pyplot as plt
import os
import yaml
from jobs import rd0, img_rd, q, add_job, get_job_by_id

app = Flask(__name__)


def get_method() -> dict:
    """
    Outputs the all data retrieved from the Redis database.
    Args:
        none
    Returns:
        data (dict): dictionary with all data from breast cancer database
    """
    try:
        if len(rd0.keys()) == 0:
            return f'Error. Breast cancer data not loaded in\n', 404
        data = []
        for item in rd0.keys():
            data.append(json.loads(rd0.get(item)))
        return data
    except Exception as err:
        return f'Error. Breast cancer data not loaded in\n', 404

def m_cases() -> int:
    """
    Returns number of malignant cases in the breast cancer database.
    Args:
        none
    Returns:
        val_m (int): number of malignant cases
    """
    try:
        val_m = 0
        for key in rd0.keys():
            m_or_b = json.loads(rd0.get(key))['Diagnosis']
            if m_or_b == 'M':
                val_m += 1
        return val_m
    except Exception as err:
        return f'Error. Breast cancer data not loaded in\n', 404

def b_cases() -> int:
    """
    Returns number of benign cases in the breast cancer database.
    Args:
        none
    Returns:
        val_m (int): number of malignant cases
    """
    try:
        val_b = 0
        for key in rd0.keys():
            m_or_b = json.loads(rd0.get(key))['Diagnosis']
            if m_or_b == 'B':
                val_b += 1
        return val_b
    except Exception as err:
        return f'Error. Breast cancer data not loaded in\n', 404
    
@app.route('/data', methods = ['POST', 'GET', 'DELETE'])
def breast_cancer_data() -> str:
    """
    Handles all available methods of 'POST', 'GET', and 'DELETE' that can be requested by the user to load, return, or delete the breast cancer data from the database. 
    Args:
        none
    Returns:
        (str): status info whether 'POST' or 'DELETE' method was executed
        data (dict): dictionary of the breast cancer data  
    """
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
            return f'Error. Breast cancer data not loaded in\n', 404
        return f'Data loaded in\n'
    elif request.method == 'GET':
        return get_method()
    elif request.method == 'DELETE':
        if len(rd0.keys()) == 0:
            return f'Error. Breast cancer data not loaded in\n', 404
        rd0.flushdb()
        return f'Data deleted\n'
    else:
        return f'No available method selected. Methods available: POST, GET, DELETE\n', 404


@app.route('/id', methods = ['GET'])
def cancer_case_id() -> list:
    """
    Returns all ID numbers representing each case within the breast cancer data.
    Args:
        none
    Returns:
        rd0.keys() (list): list of all ID numbers of the data  
    """
    if len(rd0.keys()) == 0:
        return f'Error. Breast cancer data not loaded in\n', 404
    return rd0.keys()


@app.route('/id/<id_num>', methods = ['GET'])
def id_data(id_num: int) -> dict:
    """
    Outputs data associated with <id_num> case within the breast cancer data. 
    Args:
        id_num (int): ID number value
    Returns:
        id_data (dict): data associated with <id_num>
    """
    if len(rd0.keys()) == 0:
        return f'Error. Breast cancer data not loaded in\n', 404
    try:
        id_data = json.loads(rd0.get(id_num))
        return id_data
    except Exception as err:
        return f'Error. ID {id_num} not found in database\n', 404

@app.route('/outcome', methods = ['GET'])
def get_cases() -> dict:
    """
    Returns ID numbers and total number of cases associated with diagnosis of malignant or benign.
    Args:
        none
    Returns:
        cases (dict): ID numbers and total number of malignant and benign cases
    """
    if len(rd0.keys()) == 0:
        return f'Error. Breast cancer data not loaded in\n', 404
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
        return f'Error. Breast cancer data not loaded in\n', 404

    
@app.route('/image', methods = ['POST', 'GET', 'DELETE'])
def image() -> str:
    """
    Handles all available methods of 'POST', 'GET', and 'DELETE' that can be requested by the user to load, return, or delete the graph image created utilizing the breast cancer data from the database. 
    
    Args:
        none
    Returns:
        (str): status info whether 'POST' or 'DELETE' method was executed
        image (png): image of the graph created utilizing the breast cancer data  
    """
    global rd0, img_db
    if request.method == 'POST':
        graph_data = {}
        if len(rd0.keys()) == 0:
            return f'Breast cancer data not loaded in\n', 404
        val_m = m_cases()
        val_b = b_cases()
        graph_data = {'Malignant': val_m, 'Benign': val_b}
        diagnosis = list(graph_data.keys())
        num_diagnosis = list(graph_data.values())
        plt.bar(diagnosis, num_diagnosis, color = 'maroon', width = .4)
        plt.xlabel("Diagnosis")
        plt.ylabel("Number of Cases")
        plt.title("Breast Cancer Cases Diagnosis")
        plt.savefig('./cancer_prognosis.png')
        image_data = open('./cancer_prognosis.png', 'rb').read()
        img_db.set('image', image_data)
        return f'Graph successfully saved\n'
    elif request.method == 'GET':
        if len(rd0.keys()) == 0:
            return f'Error. Breast cancer data not loaded in\n', 404
        elif len(img_db.keys()) == 0:
            return f'Error. Image not loaded in\n', 404
        try:
            image_data = rd1.get('image')
            if image_data is None:
                return f'Error. Image not loaded in\n', 404
            with open('./cancer_prognosis.png', 'wb') as image_file:
                image_file.write(image_data)
            return send_file('./cancer_prognosis.png', mimetype = 'image/png', as_attachment = True)
        except Exception as err:
            return f'Error. Unable to fetch image\n', 404
    elif request.method == 'DELETE':
        try:
            if len(img_db.keys()) == 0:
                return f'Error. Image not loaded in', 404
            img_db.flushdb()
            return f'Image deleted\n'
        except Exception as err:
            return f'Error. Unable to delete image\n', 404
    else:
        return f'No available method selected. Methods available: POST, GET, DELETE\n', 404


@app.route('/jobs', methods = ['POST'])
def api_jobs():
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
            if len(rd0.keys()) == 0:
                return 'Error. Breast cancer data not loaded in\n', 404
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
        return json.dumps(add_job(job['start'], job['end']), indent=2) + '\n'
    else:
        return f'No available method selected. Method available: POST', 404


@app.route('/jobs/<job_uuid>', methods = ['GET'])
def get_job_status(job_uuid):
    '''
    Checks the status of a submitted job.
    Args:
        job_uuid (int): job uuid number
    Returns:

    '''
    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'


@app.route('/download/<job_uuid>', methods = ['GET'])
def download(job_uuid):
    ''' dhanny's code
    if len(rd.keys()) == 0:
        return 'No data in db.\n'
    elif b'plot_image' not in img_db.keys():
        return 'Plot not in db, pls check if job is complete.\n'
    # get plot image from db
    path = './cancer_diagnosis.png'
    with open(path, 'wb') as f:
        f.write(img_db.get('plot_image'))
    return send_file(path, mimetype='image/png', as_attachment=True)
    '''

    try:
        if img_db.exists('job.'+jobid) and b'image' in img_db.hgetall('job.'+jobid):
            file_path = './{jobid}.png'
        with open(file_path, 'wb') as f:
            f.write(img_db.hget('job.'+jobid, b'image'))
        return send_file(file_path, mimetype='image/png', as_attachment=True)
    except Exception as err:
        return f'Error. Invalid job id', 404

@app.route('/help', methods = ['GET'])
def all_routes() -> str:
    '''
    Function returns help text (as a string) that briefly describes each route.
    Args:
        None
    Returns:
        help_str (str):  Help text that briefly describes each route
    '''
    help_str = '''
    Usage: curl [host_name]:5000[ROUTE]
    A Flask REST API for querying and returning interesting information from the breast cancer prognosis dataset.
    Route                           Method  What it returns
    /data                           POST    Put data into Redis database
    /data                           GET     Return entire data set from Redis database
    /data                           DELETE  Delete data in Redis database
    /id                             GET     Return json-formatted list of all "ID Number"
    /id/<id_num>                    GET     Return all data associated with <id_num>
    /image                  	    POST    Creates a plot and saves it to Redis
    /outcome	                    GET	    Return a dictionary containing information regarding malignant and benign cases
    /help                           GET     Return help text that briefly describes each route
    \n'''
    return help_str

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
