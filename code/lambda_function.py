'''
These are the handlers that will be used by AWS whenever there is a trigger
'''

import json
from datetime import datetime


#used in 1st lambda handler
from divide_data import s3_break_up_file, find_most_recent_object

#used in 2nd lambda handler
from direct_write import process_s3_object_into_dynamo, write_to_text_file_in_s3

from config import lmbda_client, \
					s3_client, \
					S3_BUCKET_NAME, \
					FILE_DOWNLOAD_FUNCTION_NAME, \
					FILE_SPLIT_FUNCTION_NAME, \
					FILE_PROCESS_FUNCTION_NAME, \
					LAMBDA_ROLE, \
					HANDLER_MODULE_NAME, \
					DATA_S3_BUCKET_NAME, \
					data_s3_client


def file_split_lambda_handler(event, context):
	'''
	This handler will execute . It takes the giant
	file and splits it into smaller files that can each be processed separately.

	'''

	print("Event: ", event)

	if 'app_store' not in event:
		print("Unable to determine which app store to update. Exiting")
		return
	if event['app_store'] == 'Apple':
		prefix = '1/42apps/v0.1/production/itunes/lookup-weekly/20'
	else:
		prefix = '1/42apps/v0.1/production/playstore/lookup-weekly/20'

	file_key = find_most_recent_object(DATA_S3_BUCKET_NAME, prefix)
	obj = data_s3_client.get_object(Bucket = DATA_S3_BUCKET_NAME, Key = file_key)
	destination_s3_bucket = 'ttd-test-account-general-bucket'
	data = obj['Body']
	if 'line_number' in event:
		start_line_number = int(event['line_number'])
	else:
		start_line_number = 0
	end_line_number = s3_break_up_file(data, destination_s3_bucket, start_line_number)
	if end_line_number != 0:
		print("Data splitting not completed in this lambda. Invoking again...")
		event['line_number'] = str(end_line_number)
		event_json = json.dumps(event)
		response = lmbda_client.invoke(
			FunctionName = 'file_split_lambda',
			InvocationType = 'Event',
			Payload = event_json.encode('utf-8')
		)
		print("Next lambda invoked..")
	else:
		print("Done processing.")
		#print("Deleting file...")
		#s3_client.delete_object(Bucket = s3_bucket, Key = file_key)
		#print("File successfully deleted.")
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


def text_file_write_lambda_handler(event, context):

	if 's3_bucket' not in event:
		print("No S3 bucket detected. Exiting")
		return
	if 'app_store' not in event:
		print("No app store identification detected. Exiting")
		return

	s3_bucket = event['s3_bucket']
	app_store = event['app_store']
	write_to_text_file_in_s3(s3_bucket, app_store)
	print("Done writing table to text file.")
	return



