import pandas as pd
import sys
from config import *
import time
from query_dynamo import *

'''

parition key helps distribute data evenly, choose something that has a large range of values 
sort key can help sort additionally with the partition key

probably want to insert each row of csv as an item
'''


def create_new_table(table_name, primary_keys = None):
	start_time = time.time()
	if not primary_keys:
		#default to two colum table of app_id and ads.txt location
		table = dynamodb.create_table(
			TableName = table_name,
			KeySchema = [
				{
					'AttributeName': 'App_ID',
					'KeyType': 'HASH' #Partition Key
				}
				# {
				# 	'AttributeName': 'Title',
				# 	'KeyType': 'RANGE' #sort key
				# }
			],
			AttributeDefinitions = [
				{
					'AttributeName': 'App_ID',
					'AttributeType': 'S'

				}
				# {
				# 	'AttributeName': 'Title',
				# 	'AttributeType': 'S'
				# },
			],
			ProvisionedThroughput = {
				'ReadCapacityUnits': 100,
				'WriteCapacityUnits': 100
			}
		)
	else:
		'''
		For the scenario when we have other keys identified other than the basic standard
		'''
		pass

	table.meta.client.get_waiter('table_exists').wait(TableName = table_name)
	print("Table took ", time.time() - start_time, " seconds to create.")
	return table


def add_item_to_table(table, key, value):
	'''
	Table is a DynamoDB table
	item_information is a dict form from key to value that we add to the table

	'''
	#table = dynamodb.Table(table_name)
	item_information = {
		'App_ID': key,
		'FileLocation': value
	}
	try: 
		table.put_item(Item = item_information)
	except:
		print("Unable to insert following entry into table.")
		print("key: ", key)
		print("value: ", value)


def retrieve_item(table, keys):

	'''
	table is a DynamoDB table
	keys is the information in dict form used to retrieve the item
	'''	
	#table = dynamodb.Table(table_name)
	try:
		response = table.get_item(Key = keys)
		item = response['Item']
		return item
	except:
		print("Unable to retrieve " + keys + ". The entry may not exist.")
		return None

def update_item(table, keys, values):
	'''
	table: db table
	keys: how to access item
	values: values to update

	'''
	#table = dynamodb.Table(table_name)
	# print("table: ", table)
	# print("values: ", values)
	# print("keys: ", keys)
	# table.update_item(
	# 	Key = keys,
	# 	AttributeUpdates = values
	# 	)
	key_dict_form = {
		'App_ID': keys
	}
	values_dict_form = {
		':val1': values
	}
	#print(key_dict_form)
	#print(values_dict_form)
	try:
		response = table.update_item(
			Key = key_dict_form,
			UpdateExpression = "set FileLocation = :val1",
			ExpressionAttributeValues = values_dict_form)
	except Exception as e:
		print("Unable to update table for key: " + keys + ". Skipping.")
	#print("Response: ", response)



def delete_item(table, keys):
	'''
	deletes an item from given table using keys.
	NOTE: deleting the item does not remove the key from the table, so you can
	still access this key without it causing an error. It will just return an empty list or nothing.
	'''
	#able = dynamodb.Table(table_name)
	try:
		table.delete_item(Key = keys)
	except:
		print("Unable to delete item.")


def find_table(csv_file):
	'''
	from the csv file name, we determine which table we are modifying with the changes
	'''
	if 'google' in csv_file:
		table_name = 'Google_Play'
	elif 'apple' in csv_file:
		table_name = 'Apple_Store'	
	try:
		# response = dynamodb.describe_table(TableName = table_name)
		table = dynamodb_client.describe_table(TableName = table_name)
		table = dynamodb.Table(table_name)
	except:
		print("No table found. Creating new table...")
		table = create_new_table(table_name)

	return table

def key_exists(keys, table):
	'''
	check if the app id is already present in the table
	'''
	items = scan_ads_txt_location(table, keys)
	if len(items) > 0:
		return True
	return False


def process_csv_file(csv_file):
	print("Processing " + csv_file + ".")
	#csv_file.decode("utf-8")
	dataframe = pd.read_csv(csv_file)
	matrix = dataframe.values
	#iterate through information and update database
	print('about to find table')
	table = find_table(csv_file)
	print('found table') 
	print(table)
	#print(table.keys())
	for i in range(1, matrix.shape[0]):
		#skip first row because those are column labels.

		key = matrix[i][0]
		value = matrix[i][1]
		item_dict = {
			'App_ID': key,
			'FileLocation': value
		}
		key_dict_form = {
			'App_ID': key
		}
		if key_exists(key, table):
			'''
			update value for the key
			'''
			update_item(table, key, value)

		else:
			'''
			insert a new item into the table
			'''
			#print(table)
			add_item_to_table(table, key, value)
		#print(retrieve_item(table, key_dict_form))
	print("Finished processing " + csv_file + " into DB.")
	return 
	


def print_all_items(table):
	print(table.scan())