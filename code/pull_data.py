import requests
#from boto3.s3.transfer import S3Transfer
from config import s3, \
				s3_client, \
				S3_BUCKET_NAME,
				DATA_ACCESS_KEY,
				DATA_ACCESS_SECRET_KEY



def push_to_s3(bucket_name, data):
	bucket = s3.Bucket(Bucket = S3_BUCKET_NAME)
	exists = True
	try:
		s3.meta.client.head_bucket(Bucket = S3_BUCKET_NAME)
	except botocore.exceptions.ClientError as e:
		error_code = int(e.response['Error']['Code'])
		if error_code == 404:
			exists = False
	if not exists:
		print("Unable to access S3 bucket to store data. Exiting.")
		exit()
	#INCOMPLETE, possibly unnecessary 



def download_data(s3_bucket, file_name, destination_bucket, new_file_name):
	'''
	The data we are using is hosted in a s3 bucket, so this function transfers
	it from that bucket to a bucket of TTD. Have to figure out how to provide
	the credentials to access that company's bucket
	'''
	print("Downloading data....")
	copy_source = {
		'Bucket': s3_bucket,
		'Key': file_name
	}
	try:
		s3.meta.client.copy(copy_source, destination_bucket, new_file_name)
	except Exception as e:
		print("Unable to copy data to S3 bucket.. Exiting")
		return
	print("Data downloaded!")
	return
