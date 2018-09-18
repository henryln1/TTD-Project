"""
Takes an s3 object that is a text file and processes 
the info in a Dynamo DB Table

"""
import time
import boto3
import json

from config import MAX_BATCH_SIZE, \
				store_keywords_dict, \
				MAX_LENGTH_KEY, \
				APPLE_TEXT_FILE_KEY, \
				GOOGLE_TEXT_FILE_KEY, \
				APPLE_STORE_TABLE_NAME, \
				GOOGLE_PLAY_TABLE_NAME

from clients import s3_client, dynamodb_client

from extractor import Extractor
from write_to_dynamo import write_items_batch, find_table, add_item_to_table
from utils import parse_for_specific_parameter

def format_batch(batch):
	"""
	processes each entry in batch into a format that can be pushed to Dynamo
	"""
	return [ { 'App_ID': str(app_id), 'FileLocation': str(location) } for (app_id, location) in batch]


def s3_determine_app_store(example_data_entry): 
	#what app store does this data dump concern
	google_play_string = 'play.google.com/store'
	apple_ios_string = 'itunes.apple.com'
	tencent_string = 'tencent'
	if google_play_string in example_data_entry:
		return 'Google'
	if apple_ios_string in example_data_entry:
		return 'Apple'
	if tencent_string in example_data_entry:
		return 'Tencent'
	print('Please examine your data file. No valid app store detected.')
	return ''

def process_s3_object_into_dynamo(s3_object_key, s3_bucket, data):
	print('Processing s3 object into Dynamo...')
	app_store = s3_determine_app_store(data[0])
	if app_store == '':
		print('Exiting...')
		return
	app_id_marker, market_url_marker, seller_url, package = store_keywords_dict[app_store]	
	extractor = Extractor(seller_url, package)
	table = find_table(app_store)
	if not table:
		return
	
	current_batch = []
	for (entry_index, current_entry) in enumerate(data):
		if len(current_entry) == 0: #skip empty lines
			continue
		current_entry_json = json.loads(current_entry)
		app_id = parse_for_specific_parameter(app_id_marker, current_entry_json)
		market_url = parse_for_specific_parameter(market_url_marker, current_entry_json)
		if app_id and market_url:
			corresponding_url = extractor.look_for_ads_txt_url(current_entry)
			if len(market_url) > MAX_LENGTH_KEY: 
				#truncating if market url is too long and crashes Dynamo processing
				market_url = market_url[:MAX_LENGTH_KEY]
		else:
			#occurs when there's an empty line in the file in my testing, there may be other cases
			print('Unable to determine keys for this entry. Skipping..')
			continue

		if corresponding_url != '':
			current_batch.append(((app_id, market_url), corresponding_url))

		if len(current_batch) % MAX_BATCH_SIZE == 0:
			formatted_batch = format_batch(current_batch)
			write_items_batch(formatted_batch, table)
			current_batch = []

	if len(current_batch) > 0:
		formatted_batch = format_batch(current_batch)
		write_items_batch(formatted_batch, table)		
	print('Finished processing s3 object into Dynamo.')
	return

def write_to_text_file_in_s3(s3_bucket, app_store):
	file_key = ''
	table_name = ''
	if app_store == 'Apple':
		file_key = APPLE_TEXT_FILE_KEY
		table_name = APPLE_STORE_TABLE_NAME
	elif app_store == 'Google':
		file_key = GOOGLE_TEXT_FILE_KEY
		table_name = GOOGLE_PLAY_TABLE_NAME
	else:
		print('Invalid app store detected. Exiting')
		return

	items = dynamodb_client.scan(TableName = table_name)['Items']

	byte_form = b''
	for item in items:
		app_id = item['App_ID']['S']
		file_location = item['FileLocation']['S']
		new_line = app_id + ', ' + file_location + '\n'
		byte_form += new_line.encode('utf-8')
	try:
		response = s3_client.put_object(
			Body = byte_form,
			Bucket = s3_bucket,
			Key = file_key)
	except Exception as e:
		print(e)
		print('Unable to write to s3 object.')
		print('Exiting...')
	return


