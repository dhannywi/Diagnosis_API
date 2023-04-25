import uuid
from hotqueue import HotQueue
import redis
import os
import json


redis_ip = os.environ.get('REDIS_IP', '172.17.0.1')
if not redis_ip:
    raise Exception()

q = HotQueue("queue", host=redis_ip, port=6379, db=2)
rd0 = redis.Redis(host=redis_ip, port=6379, db=0, decode_responses=True) 
jdb = redis.Redis(host=redis_ip, port=6379, db=1)
img_rd = redis.Redis(host=redis_ip, port=6379, db=3)

def _generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def _generate_job_key(jid):
    """
    Generate the redis key from the job id to be used when storing, retrieving or updating
    a job in the database.
    """
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, start, end):
    """
    Create the job object description as a python dictionary. Requires the job id, status,
    start and end parameters.
    """
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'start': start,
                'end': end
               }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8')
           }

def _save_job(job_key, job_dict):
    """
    Save a job object in the Redis database.
    """
    jdb.hset(job_key, mapping=job_dict)

def _queue_job(jid):
    """
    Add a job to the Redis queue.
    """
    q.put(jid)

def add_job(start, end, status="submitted"):
    """
    Add a job to the Redis queue.
    """
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, start, end)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict

def get_job_by_id(job_key):
    """
    Return job from Redis.
    """
    rdb = jdb.hgetall(_generate_job_key(job_key))
    job_dict = {}
    for keys in rdb:
        if keys != b'image':
            job_dict[keys.decode('utf-8')] = rdb[keys].decode('utf-8')
    return job_dict

def update_job_status(jid, status):
    """
    Update the status of job with job id `jid` to status `status`.
    """
    job = get_job_by_id(jid)
    if job:
        job['status'] = status
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()

def get_job_start(jid):
    """
    Return start time of job.
    """
    job = get_job_by_id(jid)
    if job:
        return job['start']
    else:
        raise Exception()

def get_job_end(jid):
    """
    Return end time of job.
    """
    job = get_job_by_id(jid)
    if job:
        return job['end']
    else:
        raise Exeption()

def update_image_job(jid, image):
    """
    Update the job with the image.
    """
    job = get_job_by_id(jid)
    if job:
        job['image'] = image
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()
