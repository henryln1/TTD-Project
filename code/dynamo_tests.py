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
	assert items[0]['App_ID'] == "('Dream League Soccer 2018', 'https://play.google.com/store/apps/details?id=com.firsttouchgames.dls3')"
	

def test_query_single_location():

	table = dynamodb.Table('Google_Play')
	key = "('Dream League Soccer 2018', 'https://play.google.com/store/apps/details?id=com.firsttouchgames.dls3')"
	items = query_ads_txt_location(table, key)
	assert len(items) == 1
	assert items[0]['App_ID'] == "('Dream League Soccer 2018', 'https://play.google.com/store/apps/details?id=com.firsttouchgames.dls3')"



def run_dynamo_tests():
		print("Executing DynamoDB Tests.")
		start_time = time.time()
		test_scan_single_location()
		print("Scan tests passed.")
		test_query_single_location()
		print("Query tests passed.")
		print("All tests run. Time Elapsed: %s seconds. Program stopping. " % (time.time() - start_time))




def main():
	run_dynamo_tests()


if __name__ == "__main__":
	main()