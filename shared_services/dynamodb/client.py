import boto3
import os
from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

TABLE_NAME = os.getenv("TABLE_NAME", "jobs")

# For infra
dynamodb_client: DynamoDBClient = boto3.client("dynamodb")

# For job handling
dynamodb_resource: DynamoDBServiceResource = boto3.resource("dynamodb")
dynamodb_table: Table = dynamodb_resource.Table(TABLE_NAME)

