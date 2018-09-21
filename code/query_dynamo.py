import boto3
from boto3.dynamodb.conditions import Attr, Key

"""
list of functions to query and look for information from a dynamo db table
"""


def scan_ads_txt_location(table, key):

	"""
	Given the key form of a mobile app id, we look in the table for it's ads.txt location
	"""
	try:
		response = table.scan(FilterExpression = Attr('App_ID').eq(key))
		items = response['Items']
		return items
	except Exception as e:
		print('Unable to query table for this mobile app id.')
		print(e)		
		return None


def query_ads_txt_location(table, key):
	"""
	According to AWS DynamoDB documentation, query will scale better with table size,
	so probably better to use this function versus the one above to improve speed. 
	"""

	try:
		response = table.query(
			KeyConditionExpression = Key('App_ID').eq(key)
		)
		return response['Items']
	except Exception as e:
		print('Unable to query table for this mobile app id.')
		print(e)