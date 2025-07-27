import boto3
import botocore
import os

TABLE_NAME = os.getenv("TABLE_NAME", "jobs")
ENV = os.getenv("ENV", "development")

dynamodb = boto3.client("dynamodb")

def table_exists(table_name):
    try:
            dynamodb.describe_table(TableName=table_name)
            print(f"Table '{table_name}' already exists.")
            return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table '{table_name}' does not exist.")
            return False
        else:
            raise

    
# def delete_table(table_name):
#     print(f" Deleting table '{table_name}' ...")
#     dynamodb.delete_table(TableName=table_name)
#     dynamodb.get_waiter('table_not_exists').wait(TableName=table_name)
#     print("Table deleted.")

def create_table(table_name):
    print(f"Creating table '{table_name}'...")
    dynamodb.create_table(
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
    dynamodb.get_waiter('table_exists').wait(TableName=table_name)
    print("Table created successfully.")

def init_dynamo_instance():
    if not table_exists(TABLE_NAME):
        create_table(TABLE_NAME)


if __name__ == "__main__":
    init_dynamo_instance()

