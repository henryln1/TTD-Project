"""
These are the handlers that will be used by AWS whenever there is a trigger
"""

import json
from datetime import datetime


#used in 1st lambda handler
from divide_data import s3_break_up_file, find_most_recent_object

#used in 2nd lambda handler
from direct_write import process_s3_object_into_dynamo, write_to_text_file_in_s3

from config import S3_BUCKET_NAME, \
					DATA_S3_BUCKET_NAME, \
					DATA_S3_PREFIX_GOOGLE, \
					DATA_S3_PREFIX_APPLE

from clients import s3_client, data_s3_client, lambda_client



def file_split_lambda_handler(event, context):
	"""
	This handler will execute . It takes the giant
	file and splits it into smaller files that can each be processed separately.

	"""
	def fetch_most_recent_data(event):
		if 'app_store' not in event:
			print('Unable to determine which app store to update. Exiting')
			return None, 0
		start_line_number = int(event.get('line_number', '0'))
		if event['app_store'] == 'Apple':
			prefix = DATA_S3_PREFIX_APPLE
		else:
			prefix = DATA_S3_PREFIX_GOOGLE
		file_key = find_most_recent_object(DATA_S3_BUCKET_NAME, prefix)
		obj = data_s3_client.get_object(Bucket = DATA_S3_BUCKET_NAME, Key = file_key)
		return (obj['Body'], start_line_number)

	def reschedule_lambda(event, end_line_number):
		print('Data splitting not completed in this lambda. Invoking again...')
		event['line_number'] = str(end_line_number)
		event_json = json.dumps(event)
		response = lambda_client.invoke(
			FunctionName = 'file_split_lambda',
			InvocationType = 'Event',
			Payload = event_json.encode('utf-8')
		)
		print('Next lambda invoked..')		

	print('Event: ', event)
	(data, start_line_number) = fetch_most_recent_data(event)
	if not data:
		return
	end_line_number = s3_break_up_file(data, destination_s3_bucket, start_line_number)
	if end_line_number != 0:
		reschedule_lambda(event, end_line_number)
	else:
		print('Done processing.')
	return


def process_into_dynamo_lambda_handler(event, context):
	"""
	Triggers whenever a smaller file is occurred (from the above handler) and
	runs url extraction and then writes that information into amazon dynamodb.
	Since this triggers whenever a smaller file is created, there will be many of these
	running concurrently, not in sequential order. 
	"""

	def get_data(s3_bucket, file_key):
		print('File key: ', file_key)
		print('S3 bucket: ', s3_bucket)
		obj = s3_client.get_object(Bucket = s3_bucket, Key = file_key)
		rows_of_data = obj['Body'].read().decode().split('\n')
		return rows_of_data

	def delete_object(s3_bucket, file_key):
		print('Deleting file...')
		s3_client.delete_object(Bucket = s3_bucket, Key = file_key)
		print('File successfully deleted.')


	file_key = event['Records'][0]['s3']['object']['key']
	s3_bucket = event['Records'][0]['s3']['bucket']['name']
	rows_of_data = get_data(s3_bucket, file_key)
	process_s3_object_into_dynamo(file_key, s3_bucket, rows_of_data)
	delete_object(s3_bucket, file_key)

	return


def text_file_write_lambda_handler(event, context):

	if 's3_bucket' not in event:
		print('No S3 bucket detected. Exiting.')
		return
	if 'app_store' not in event:
		print('No app store identification detected. Exiting.')
		return

	s3_bucket = event['s3_bucket']
	app_store = event['app_store']
	write_to_text_file_in_s3(s3_bucket, app_store)
	print('Done writing table to text file.')
	return



