import boto3
import os

TABLE_NAME = os.getenv("TABLE_NAME", "jobs")

# For infra
dynamodb_client = boto3.client("dynamodb")

# For job handling
dynamodb_resource = boto3.resource("dynamodb")
dynamodb_table = dynamodb_resource.Table(TABLE_NAME)

