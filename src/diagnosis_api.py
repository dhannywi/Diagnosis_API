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

@app.route('/diagnosis-mean-radius', methods = ['GET'])
def get_details() -> dict:
    '''
    Returns information on mean radius max, min and avg, based on diagnosis
    Args:
        None
    Returns:
        data_dict (dict): Nested dictionary containing mean radius information based on diagnosis
    '''
    if len(rd0.keys()) == 0:
        return f'Error. Breast cancer data not loaded in\n', 404
    
    data_dict = {'Malignant': {'cases': 0, 'mean_radius': {} }, 'Benign': {'cases': 0, 'mean_radius': {} } }
    mean_rad_M = []
    mean_rad_B = []
    for key in rd0.keys():
        diagnosis = json.loads(rd0.get(key))['Diagnosis']
        if diagnosis == 'M':
            data_dict['Malignant']['cases'] += 1
            mean_rad_M.append(float(json.loads(rd0.get(key))['Mean Radius']))
        elif diagnosis == 'B':
            data_dict['Benign']['cases'] += 1
            mean_rad_B.append(float(json.loads(rd0.get(key))['Mean Radius']))

    data_dict['Malignant']['mean_radius']['max'] = max(mean_rad_M)
    data_dict['Malignant']['mean_radius']['min'] = min(mean_rad_M)
    data_dict['Malignant']['mean_radius']['avg'] = round(sum(mean_rad_M)/len(mean_rad_M), 2)

    data_dict['Benign']['mean_radius']['max'] = max(mean_rad_B)
    data_dict['Benign']['mean_radius']['min'] = min(mean_rad_B)
    data_dict['Benign']['mean_radius']['avg'] = round(sum(mean_rad_B)/len(mean_rad_B), 2)
    return data_dict



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
    global rd0, img_rd
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
        elif len(img_rd.keys()) == 0:
            return f'Error. Image not loaded in\n', 404
        try:
            image_data = img_rd.get('image')
            if image_data is None:
                return f'Error. Image not loaded in\n', 404
            with open('./cancer_prognosis.png', 'wb') as image_file:
                image_file.write(image_data)
            return send_file('./cancer_prognosis.png', mimetype = 'image/png', as_attachment = True)
        except Exception as err:
            return f'Error. Unable to fetch image\n', 404
    elif request.method == 'DELETE':
        try:
            if len(img_rd.keys()) == 0:
                return f'Error. Image not loaded in', 404
            img_db.flushdb()
            return f'Image deleted\n'
        except Exception as err:
            return f'Error. Unable to delete image\n', 404
    else:
        return f'No available method selected. Methods available: POST, GET, DELETE\n', 404


@app.route('/jobs', methods = ['POST', 'GET'])
def api_jobs():
    """
    Allows use to submit job to the worker.
    Args:
        none
    Returns:
        results (dict): submits job to worker with given arguments by user
    """
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
            if len(rd0.keys()) == 0:
                return 'Error. Breast cancer data not loaded in\n', 404
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.\n'.format(e)})
    
        return json.dumps(add_job(job['start'], job['end']), indent=2) + '\n'
    else:
        return f'No available method selected. Method available: POST\n', 404


@app.route('/jobs/<job_id>', methods = ['GET'])
def get_job_status(job_id):
    """
    Checks the status of a submitted job.
    Args:
        job_id (str): job ID number
    Returns:
        results (dict): status of submitted job
    """
    return json.dumps(get_job_by_id(job_id), indent=2) + '\n'


@app.route('/download/<job_id>', methods = ['GET'])
def download(job_id):
    """
    Downloads the image generated by the jobs route.
    Args:
        job_id (str): job ID number
    Returns:
        results (png): image created by the job ID
    """
    try:
        path = f'/app{job_id}.png'
        with open(path, 'wb') as f:
            f.write(img_rd.hget(job_id, 'image'))
        return send_file(path, mimetype = 'image/png', as_attachment = True)
    except Exception as err:
        return f'Error. Invalid job id\n', 404

    
@app.route('/help', methods = ['GET'])
def all_routes() -> str:
    """
    Function returns help text (as a string) that briefly describes each route.
    Args:
        None
    Returns:
        help_str (str):  Help text that briefly describes each route
    """
    help_str = '''
    Usage: curl [host_name]:5000[ROUTE]
    A Flask REST API for querying and returning interesting information from the breast cancer diagnosis dataset.
    Route                           Method  What it returns
    /data                           POST    Put data into Redis database
    /data                           GET     Return entire data set from Redis database
    /data                           DELETE  Delete data in Redis database
    /id                             GET     Return json-formatted list of all "ID Number"
    /id/<id_num>                    GET     Return all data associated with <id_num>
    /outcome	                    GET	    Return a dictionary with information on malignant and benign cases with associated ID Numbers
    /diagnosis-mean-radius          GET     Return a dictionary with Mean Radius information based on diagnosis
    /image                  	    POST    Creates a plot and saves it to Redis
    /image                  	    GET     Returns the plot created
    /image                  	    DELETE  Delete the plot saved in Redis database
    /jobs                           POST    Submits job to worker for analysis of data
    /jobs/<job_id>                  GET     Returns the status of the <job_id>
    /download/<job_id>              GET     Returns the plot associated with <job_id>
    /help                           GET     Return help text that briefly describes each route

    \n'''
    return help_str

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
