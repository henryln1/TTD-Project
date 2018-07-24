import boto3
import time
from boto3.dynamodb.conditions import Attr, Key

'''
list of functions to query and look for information from a dynamo db table
'''



dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://localhost:8000/')



def scan_ads_txt_location(table, key):

	'''
	Given the key form of a mobile app id, we look in the table for it's ads.txt location
	'''

	response = table.scan(FilterExpression = Attr('App_ID').eq(key))
	items = response['Items']
	return items

def query_ads_txt_location(table, key):
	'''
	According to AWS DynamoDB documentation, query will scale better with table size,
	so probably better to use this function versus the one above to improve speed. 

	'''

	response = table.query(
		KeyConditionExpression = Key('App_ID').eq(key))

	return response['Items']