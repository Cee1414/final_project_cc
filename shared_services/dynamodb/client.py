# shared_services/dynamodb/client.py
import os
import boto3

# Table + config from environment
TABLE_NAME = os.getenv("TABLE_NAME", "jobs")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")  # set in docker-compose for local

# Low-level client (used by init_utils for describe/create/waiters)
dynamodb_client = boto3.client(
    "dynamodb",
    region_name=REGION,
    endpoint_url=ENDPOINT_URL
)

# High-level resource table (used by job_io for put/get/update/scan)
_dynamodb_resource = boto3.resource(
    "dynamodb",
    region_name=REGION,
    endpoint_url=ENDPOINT_URL
)
dynamodb_table = _dynamodb_resource.Table(TABLE_NAME)
