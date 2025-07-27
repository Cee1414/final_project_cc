from shared_services.dynamodb.client import dynamodb_table


def push_job(job):
    dynamodb_table.put_item(Item=job)

def delete_job(job_id):
    dynamodb_table.delete_item(Key={"job_id": job_id})
        
def get_all_jobs():
    return dynamodb_table.scan()