'''
Takes an s3 object that is a text file and processes 
the info in a Dynamo DB Table

'''

import sys
import time
import boto3
import os

from config import MAX_BATCH_SIZE, store_keywords_dict, MAX_LENGTH_KEY
from check_url import *
from extractor import Extractor
from write_to_dynamo import write_items_batch, find_table, add_item_to_table
from utils import parse_for_specific_parameter

def format_batch(batch):
	'''
	processes each entry in batch into a format that can be pushed to Dynamo
	'''
	formatted = []
	for item in batch:
		app_id, location = item
		formatted_item = {
			'App_ID': str(app_id),
			'FileLocation': str(location) 
		}
		formatted.append(formatted_item)
	return formatted

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
	print("Please examine your data file. No valid app store detected.")
	return ''


def process_s3_object_into_dynamo(s3_object_key, s3_bucket, data):
	print("Processing s3 object into Dynamo...")
	app_store = s3_determine_app_store(data[0])
	if app_store == '':
		print("Exiting...")
		exit()
	app_id_marker, market_url_marker, seller_url, package = store_keywords_dict[app_store]	
	extractor = Extractor(seller_url, package)
	table = find_table(app_store)
	
	current_batch = []
	for entry_index in range(len(data)):
		current_entry = data[entry_index]
		app_id = parse_for_specific_parameter(app_id_marker, current_entry)
		market_url = parse_for_specific_parameter(market_url_marker, current_entry)
		if app_id and market_url:
			corresponding_url = extractor.look_for_ads_txt_url(current_entry)
			if len(market_url) > MAX_LENGTH_KEY: 
				#truncating if market url is too long and crashes Dynamo processing
				market_url = market_url[:MAX_LENGTH_KEY]
		else:
			#occurs when there's an empty line in the file in my testing, there may be other cases
			print("Unable to determine keys for this entry. Skipping..")
			continue
		if corresponding_url == '':
			corresponding_url = 'No ads.txt file found.'

		current_batch.append(((app_id, market_url), corresponding_url))

		if len(current_batch) % MAX_BATCH_SIZE == 0:
			formatted_batch = format_batch(current_batch)
			write_items_batch(formatted_batch, table)
			current_batch = []

	print("Finished processing s3 object into Dynamo.")
	return





def main2(args):
	directory = args[1]
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		print(filename)
		process_file_into_dynamo(directory + '/' + filename)

def main(args):
	start_time = time.time()
	process_file_into_dynamo(args[1])
	print("Processing file took ", time.time() - start_time, " seconds.")


if __name__ == "__main__":
	main2(sys.argv)





