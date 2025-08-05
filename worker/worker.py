from shared_services.redis import queue
from shared_services.dynamodb import job_io
from decimal import Decimal, Overflow
import json
import time
import jobs

while True:
    raw_job = queue.pop_job(block=True, timeout=10)  # wait up to 10s
    if not raw_job:
        # timed out waiting; loop again (quietly)
        continue

    job = json.loads(raw_job)
    job_id = job.get("job_id")
    job_name = job.get("task")
    i = job.get("input")
    
    job_name = i['task']
    user_input = i['user_input']
    file_input = i['file']
    hash_type = i['hash_type']

    job_io.update_field(job_id, "status", "in-progress")
    print(f"starting job: '{job_id}'")

    outputValue = jobs.start_job(job_name, user_input, file_input, hash_type)
    job_io.update_field(job_id, "output", outputValue)
    
    '''
    try:
        job_io.update_field(job_id, "output", outputValue)
    except Overflow as e: 
        print("ERROR: {}".format(e))
        job_io.update_field(job_id, "status", "failed")
        job_io.delete_job(job_id)
        queue.pop_job()  # I thought this wombo combo would work but the job persists.
        break
    '''
    job_io.update_field(job_id, "status", "completed")
    print("job finished")
