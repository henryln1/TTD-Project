'''
These are the handlers that will be used by AWS whenever there is a trigger
From my current understanding, a trigger will execute the corresponding
function whenever it occurs, so I just need to put what code I want to run
in corresponding handler
'''

from datetime import datetime


#used in 1st lambda handler
from pull_data import download_data

#used in 2nd lambda handler
from divide_data import s3_break_up_file

#used in 3rd lambda handler
from direct_write import process_s3_object_into_dynamo

from config import lmbda_client, \
					s3_client, \
					S3_BUCKET_NAME, \
					FILE_DOWNLOAD_FUNCTION_NAME, \
					FILE_SPLIT_FUNCTION_NAME, \
					FILE_PROCESS_FUNCTION_NAME, \
					LAMBDA_ROLE, \
					HANDLER_MODULE_NAME, \
					DATA_S3_BUCKET_NAME

def file_download_lambda_handler(event, context):
	'''
	event is in the form of dict that passes event data to handler
	context is of type LambdaContext, contains runtime information

	Documentation: https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
	'''

	'''
	This handler should be on a scheduled trigger, occurrly either daily or weekly.
	It should then download the data dump from 42matters.
	'''
	print("Event: ", event)
	source_bucket = DATA_S3_BUCKET_NAME
	destination_bucket = S3_BUCKET_NAME
	destination_bucket = 'ttd-test-account-general-bucket'
	app_store = event['app_store']
	folder = ''
	if app_store == 'Apple':
		folder = 'itunes'
	elif app_store == 'Google':
		folder = 'playstore'

	destination_file_key = 'app_metadata_' + str(datetime.now()) + '_' + folder
	directory_root = '1/42apps/v0.1/production/'
	source_file_key = directory_root + folder + '/lookup-weekly/2018-09-04/itunes-00.tar.gz'
	print(source_file_key)
	#data_location = event['data_location']
	download_data(source_bucket, source_file_key, destination_bucket, destination_file_key)
	return


def file_split_lambda_handler(event, context):
	'''
	This handler will execute upon the dump being downloaded. It takes the giant
	file and splits it into smaller files that can each be processed separately.

	'''

	
	file_key = event['Records'][0]['s3']['object']['key']
	s3_bucket = event['Records'][0]['s3']['bucket']['name']
	obj = s3_client.get_object(Bucket = s3_bucket, Key = file_key)
	#rows_of_data = obj['Body'].read().decode().split('\n')

	data = obj['Body']

	s3_break_up_file(data, s3_bucket)
	print("Deleting file...")
	s3_client.delete_object(Bucket = s3_bucket, Key = file_key)
	print("File successfully deleted.")
	return

def process_into_dynamo_lambda_handler(event, context):
	'''
	Triggers whenever a smaller file is occurred (from the above handler) and
	runs url extraction and then writes that information into amazon dynamodb.
	Since this triggers whenever a smaller file is created, there will be many of these
	running concurrently, not in sequential order. 


	'''

	file_key = event['Records'][0]['s3']['object']['key']
	s3_bucket = event['Records'][0]['s3']['bucket']['name']
	print("File key: ", file_key)
	print("S3 bucket: ", s3_bucket)
	obj = s3_client.get_object(Bucket = s3_bucket, Key = file_key)
	rows_of_data = obj['Body'].read().decode().split('\n')
	process_s3_object_into_dynamo(file_key, s3_bucket, rows_of_data)
	print("Deleting file...")
	s3_client.delete_object(Bucket = s3_bucket, Key = file_key)
	print("File successfully deleted.")
	return