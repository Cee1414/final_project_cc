import boto3
import os

TABLE_NAME = os.getenv("TABLE_NAME", "jobs")

dynamodb = boto3.client("dynamodb")
