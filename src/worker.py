from jobs import update_image_job, update_job_status, q, rd0, jdb, img_rd, get_job_start, get_job_end
import time
import matplotlib.pyplot as plt
import redis
import os
import json
from hotqueue import HotQueue


@q.worker
def execute_job(jid):
    """
    Executes job for the given <jid>.
    Args:
        jid (): jod ID number
    Returns:
        none
    """
    if len(rd0.keys()) == 0:
        return f'Error. Breast cancer data not loaded in\n', 404
    else:
        update_job_status(jid, 'in progress')
        start = float(get_job_start(jid))
        end = float(get_job_end(jid))
        graph_data = {'Malignant': 0, 'Benign': 0}
        for key in rd0.keys():
            val = float(json.loads(rd0.get(key))['Mean Radius'])
            if val >= start and val <= end:
                diagnosis = json.loads(rd0.get(key))['Diagnosis']
                if diagnosis == 'M':
                    graph_data['Malignant'] += 1
                elif diagnosis == 'B':
                    graph_data['Benign'] += 1

        x = [i for i in graph_data.keys()]
        y = [i for i in graph_data.values()]
        plt.bar(x, y, color = 'lightblue', width = .4)
        plt.xlabel("Diagnosis")
        plt.ylabel("Number of Cases")
        plt.title("Breast Cancer Cases Diagnosis")
        plt.savefig('./cancer_diagnosis.png')
        
        with open('./cancer_diagnosis.png', 'rb') as f:
            img = f.read()
        img_rd.hset(jid, 'image', img)
        update_image_job(jid, img)
        update_job_status(jid, 'complete')       

        
execute_job()
