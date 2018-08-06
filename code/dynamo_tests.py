import boto3
from query_dynamo import *
from write_to_dynamo import *
import time

'''
Tests to make sure DynamoDB functions are working correctly.

'''






def test_scan_single_location():
	table = dynamodb.Table('Google_Play')
	key = "('Dream League Soccer 2018', 'https://play.google.com/store/apps/details?id=com.firsttouchgames.dls3')"
	items = scan_ads_txt_location(table, key)

	assert len(items) == 1
	print("location", items[0]['FileLocation'])
	assert items[0]['App_ID'] == "('Dream League Soccer 2018', 'https://play.google.com/store/apps/details?id=com.firsttouchgames.dls3')"
	

def test_query_single_location():

	table = dynamodb.Table('Google_Play')
	key = "('Dream League Soccer 2018', 'https://play.google.com/store/apps/details?id=com.firsttouchgames.dls3')"
	items = query_ads_txt_location(table, key)
	assert len(items) == 1
	assert items[0]['App_ID'] == "('Dream League Soccer 2018', 'https://play.google.com/store/apps/details?id=com.firsttouchgames.dls3')"

def single_item_to_table_test():
	table = dynamodb.Table('Apple_Store')
	item = {
		'App_ID': "('eBay Inc.', 'http://itunes.apple.com/artist/ebay-inc/id282614219?uo=5')",
		'FileLocation': 'No ads.txt found.'
	}
	key = item['App_ID']
	value = item['FileLocation']
	add_item_to_table(table, key, value)

	assert len(scan_ads_txt_location(table, key)) == 1 
	
	key_dict_form = {
		'App_ID': key
	}
	retrieved_item = retrieve_item(table, key_dict_form)
	assert item == retrieved_item
	values_to_update_dict_form = {
		':l': 'No ads.txt found modified.'
	}
	update_item(table, key_dict_form, values_to_update_dict_form)
	delete_item(table, key_dict_form)
	assert key_exists(key, table) is False





def run_dynamo_tests():
		print("Executing DynamoDB Tests.")
		start_time = time.time()
		test_scan_single_location()
		print("Scan tests passed.")
		test_query_single_location()
		print("Query tests passed.")
		single_item_to_table_test()
		print("Item addition tests passed.")
		print("All tests run. Time Elapsed: %s seconds. Program stopping. " % (time.time() - start_time))




def main():
	run_dynamo_tests()


if __name__ == "__main__":
	main()