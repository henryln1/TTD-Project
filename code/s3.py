import boto3
from config import S3_BUCKET_NAME


# prints out the names of all the buckets we have
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
	print(bucket.name)