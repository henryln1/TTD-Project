
import boto3
from config import DATA_ACCESS_KEY, DATA_SECRET_ACCESS_KEY, S3_REGION


dynamodb_resource = boto3.resource('dynamodb', region_name = S3_REGION)

dynamodb_client = boto3.client('dynamodb')

s3 = boto3.resource('s3')

s3_client = boto3.client('s3')

lambda_client = boto3.client('lambda')

data_s3_client = boto3.client(
    's3',
    aws_access_key_id = DATA_ACCESS_KEY,
    aws_secret_access_key = DATA_SECRET_ACCESS_KEY,
    use_ssl=True)

