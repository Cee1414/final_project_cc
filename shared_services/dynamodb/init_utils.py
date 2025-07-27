from shared_services.dynamodb.client import dynamodb_client, TABLE_NAME
import botocore


def table_exists(table_name):
    try:
            dynamodb_client.describe_table(TableName=table_name)
            print(f"Table '{table_name}' already exists.")
            return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table '{table_name}' does not exist.")
            return False
        else:
            raise

def delete_table(table_name):
    print(f" Deleting table '{table_name}' ...")
    dynamodb_client.delete_table(TableName=table_name)
    dynamodb_client.get_waiter('table_not_exists').wait(TableName=table_name)
    print("Table deleted.")

def create_table(table_name):
    print(f"Creating table '{table_name}'...")
    dynamodb_client.create_table(
        TableName=table_name,
        BillingMode="PAY_PER_REQUEST",
        #define attribute structure
        AttributeDefinitions=[
            {"AttributeName": "job_id", "AttributeType": "S"}
        ],
        #define if partition or index
        KeySchema=[
            {"AttributeName": "job_id", "KeyType": "HASH"}
        ]
    )
    dynamodb_client.get_waiter('table_exists').wait(TableName=table_name)
    print("Table created successfully.")

def init_dynamo_instance():
    if not table_exists(TABLE_NAME):
        create_table(TABLE_NAME)