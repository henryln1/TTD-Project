"""
Takes an s3 object that is a text file and processes 
the info in a Dynamo DB Table

"""
import time
import boto3
import json

from config import MAX_BATCH_SIZE, \
				MAX_LENGTH_KEY, \
				all_stores

from clients import s3_client, \
				dynamodb_client

from extractor import Extractor
from write_to_dynamo import find_table, add_item_to_table


def s3_determine_app_store(example_data_entry): 
	"""Return the store id from which this data entry was taken"""
	for (store_id, store_config) in all_stores.items():
		if store_config['identifyingString'] in example_data_entry:
			return store_id
	print('Please examine your data file. No valid app store detected.')
	return ''

def process_s3_object_into_dynamo(s3_object_key, s3_bucket, data):
	"""
	Iterates through data and writes it into DynamoDB table
	"""
	print('Processing s3 object into Dynamo...')
	app_store = s3_determine_app_store(data[0])
	if app_store == '':
		print('Exiting...')
		return
	app_id_marker, market_url_marker, seller_url, package = all_stores[app_store]['keywords']
	extractor = Extractor(seller_url, package)
	table = find_table(app_store)
	if not table:
		return
	
	for current_entry in data:
		if len(current_entry) == 0: #skip empty lines
			continue
		try:
			current_entry_json = json.loads(current_entry)
		except Exception as e:
			print(e)
			continue
		app_id = current_entry_json.get(app_id_marker, '')
		market_url = current_entry_json.get(market_url_marker, '')
		if app_id and market_url:
			corresponding_url = extractor.look_for_ads_txt_url(current_entry_json)
			if len(market_url) > MAX_LENGTH_KEY: 
				#truncating if market url is too long and crashes Dynamo processing
				market_url = market_url[:MAX_LENGTH_KEY]
		else:
			#occurs when there's an empty line in the file in my testing, there may be other cases
			print('Unable to determine keys for this entry. Skipping..')
			continue
		if corresponding_url != '':
			add_item_to_table(table, (app_id, market_url), corresponding_url)		
	print('Finished processing s3 object into Dynamo.')



def write_to_text_file_in_s3(s3_bucket, app_store):
	"""
	Takes DynamoDB table and writes it to S3 in the form of a text file.
	"""
	file_key = ''
	table_name = ''

	if app_store in all_stores:
		file_key = all_stores[app_store]['storageBucketKeyName']
		table_name = all_stores[app_store]['tableName']
	else:
		print('Invalid app store detected. Exiting')
		return

	response_dynamo = dynamodb_client.scan(TableName = table_name)
	byte_form = b''
	#a bit iffy about having two for loops doing same thing but following structure of AWS documentation
	#https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html

	for item in response_dynamo['Items']:
		app_id = item['App_ID']['S']
		file_location = item['FileLocation']['S']
		new_line = app_id + ', ' + file_location + '\n'	
		byte_form += new_line.encode('utf-8')	

	while 'LastEvaluatedKey' in response_dynamo:
		response_dynamo = dynamodb_client.scan(TableName = table_name, 
			ExclusiveStartKey= response_dynamo['LastEvaluatedKey'])

		for item in response_dynamo['Items']:
			app_id = item['App_ID']['S']
			file_location = item['FileLocation']['S']
			new_line = app_id + ', ' + file_location + '\n'	
			byte_form += new_line.encode('utf-8')

	try:
		response = s3_client.put_object(
			Body = byte_form,
			Bucket = s3_bucket,
			ContentLength = len(byte_form),
			Key = file_key)
	except Exception as e:
		print(e)
		print('Unable to write to s3 object.')
		print('Exiting...')



