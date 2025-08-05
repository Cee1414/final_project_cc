from shared_services.dynamodb.client import dynamodb_table

def get_job(job_id: str):
    resp = dynamodb_table.get_item(Key={"job_id": job_id})
    return resp.get("Item")

def push_job(job):
    dynamodb_table.put_item(Item=job)

def delete_job(job_id):
    dynamodb_table.delete_item(Key={"job_id": job_id})
        
def get_all_jobs():
    return dynamodb_table.scan()

def update_field(job_id, field, value):
    # Use placeholder names to avoid issues with reserved keywords (e.g., 'status', 'type')
    placeholder_name = f"#{field}"   # placeholder for the attribute name
    placeholder_value = f":{field}"  # placeholder for the new value

    dynamodb_table.update_item(
        Key={"job_id": job_id},  # Identify the item to update by primary key

        # Use a parameterized SET expression to safely update the field
        # Placeholders allow you to avoid reserved keyword conflicts and injection risks
        UpdateExpression=f"SET {placeholder_name} = {placeholder_value}",

        # Maps the placeholder to the actual field name (e.g., '#status' -> 'status')
        ExpressionAttributeNames={placeholder_name: field},

        # Maps the placeholder to the actual value (e.g., ':status' -> 'done')
        ExpressionAttributeValues={placeholder_value: value}
    )
