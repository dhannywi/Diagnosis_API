from jobs import q, update_job_status, rd0, jdb, img_rd
import time
import matplotlib.pyplot as plt
import redis
import os
import json
from hotqueue import HotQueue
#from diagnosis_api import m_cases
#from diagnosis_api import b_cases

#redis_ip = os.environ.get('REDIS_IP')
#if not redis_ip:
#    redis Exception()

    
#rd0 = redis.Redis(host=redis_ip, port=6369, db=0, decode_responses=True)
#q = HotQueue('queue', host=redis_ip port=6379, db=2)
#rd1 = redis.Redis(host=redis_ip, port=6379, db=1)

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    time.sleep(15)
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

    with open('./cancer_prognosis.png', 'rb') as f:
        image_data = f.read()
    rd1.hset(jid, 'image', image_data)
    
    update_job_status(jid, 'complete')

execute_job()
