from jobs import update_image_job, update_job_status, q,rd0, jdb, img_rd
import time
import matplotlib.pyplot as plt
import redis
import os
import json
from hotqueue import HotQueue


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


@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    if len(rd0.keys()) == 0:
        return f'Error. Breast cancer data not loaded in\n', 404
    else:
        graph_data = {}
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
        plt.clf()
        image_file = open('./cancer_prognosis.png', 'rb').read()
        img_rd.set('plot_image', image_file)
        update_image_job(jid, image_file)
    update_job_status(jid, 'complete')

execute_job()
