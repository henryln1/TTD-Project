'''
Experimental method of processing and writing directl into DynamoDB.
Implementing so we can test the time it takes compared to first writing it
into a csv file.

'''

from config import MAX_BATCH_SIZE, store_keywords_dict
from check_url import *
from extractor import *
from write_to_dynamo import write_items_batch
from utils import parse_for_specific_parameter




'''
Functions include manually defined variables for now while we get set up and running.
Will update to make it flexible later
'''


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


def process_file_into_dynamo(file_name):
	app_store = 'Apple_Store'
	app_id_marker, market_url, seller_url, package = store_keywords_dict[app_store]	
	extractor = Extractor(seller_url, package)

	table = None

	with open(file_name, 'r', encoding = 'utf-8') as f:
		current_entry = f.readline()
		current_batch = []
		while current_entry:
			app_id = parse_for_specific_parameter(app_id_marker, current_entry)[0]
			market_url = parse_for_specific_parameter(market_url_marker, current_entry)[0]

			if app_id and market_url:
				corresponding_url = extractor.look_for_ads_txt_url(current_entry)
			current_batch.append(((app_id, market_url), corresponding_url))

			if len(current_batch) % MAX_BATCH_SIZE == 0:
				formatted_batch = format_batch(current_batch)
				write_items_batch(formatted_batch, table)
				current_batch = [] #empty out the current batch







