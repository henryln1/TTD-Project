import requests
from datetime import datetime, timedelta
#from boto3.s3.transfer import S3Transfer
from config import s3, \
				s3_client, \
				S3_BUCKET_NAME, \
				DAYS_IN_CYCLE, \
				data_s3_client


def download_data(source_s3_bucket, source_file_name, destination_bucket, destination_file_name):
	'''
	The data we are using is hosted in a s3 bucket, so this function transfers
	it from that bucket to a bucket of TTD. 
	'''

	print("Downloading data....")
	copy_source = {
		'Bucket': source_s3_bucket,
		'Key': source_file_name
	}
	date_N_days_ago = datetime.now() - timedelta(days = DAYS_IN_CYCLE)
	try:
		data_s3_client.copy(
			copy_source,
			'destination_bucket',
			'destination_file_name')
		# data_s3_client.copy_object(Bucket = destination_bucket, 
		# 	CopySource = copy_source,
		# 	CopySourceIfModifiedSince = date_N_days_ago,
		# 	Key = destination_file_name)
	except Exception as e:
		print("Unable to copy data to S3 bucket.. Exiting")
		print(e)
		return
	
	print("Data downloaded!")
	return
