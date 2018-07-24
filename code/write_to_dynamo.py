import boto3
import time
import pandas as pd 

# import os
# os.environ["TZ"] = "UTC"




dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://localhost:8000/')


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


def add_item_to_table(table, item_information):
	'''
	Table is a DynamoDB table
	item_information is a dict form from key to value that we add to the table

	'''

	table.put_item(Item = item_information)


def retrieve_item(table, keys):

	'''
	table is a DynamoDB table
	keys is the information in dict form used to retrieve the item
	'''	
	response = table.get_item(Key = keys)
	item = response[item]
	return item

def update_item(table, keys, values):
	'''
	table: db table
	keys: how to access item
	values: values to update

	'''
	table.update_item(
		Key = keys,
		UpdateExpression = ' SET Location = No ads.txt found.',
		ExpressionAttributeValues = values
		)
	

def delete_item(table, keys):
	'''
	deletes an item from given table using keys
	'''
	table.delete_item(Key = keys)


def find_table(csv_file):
	'''
	from the csv file name, we determine which table we are modifying with the changes
	'''
	if 'google' in csv_file:
		table_name = 'Google_Play'
	else:
		table_name = 'Apple_Store'
	
	try:
		# response = dynamodb.describe_table(TableName = table_name)
		table = dynamodb.Table(table_name)
	except:
		table = create_new_table(table_name)

	return table

def key_exists(keys, table):
	'''
	check if the app id is already present in the table. if it is, we update it
	'''
	try:
		item = table.get_item(Key = keys)
	except:
		return False
	return True


def process_csv_file(csv_file):
	print("Processing " + csv_file + ".")
	#csv_file.decode("utf-8")
	dataframe = pd.read_csv(csv_file)
	matrix = dataframe.values
	#iterate through information and update database

	table = find_table(csv_file) 
	for i in range(1, matrix.shape[0]):
		#skip first row because those are column labels.

		key = matrix[i][0]
		value = matrix[i][1]
		item_dict = {
			'App_ID': key,
			'Location': value
		}
		if key_exists(key, table):
			'''
			update value for the key
			'''
			update_item(table, key)

		else:
			'''
			insert a new item into the table
			'''
			add_item_to_table(table, item_dict)

	print("Finished processing " + csv_file + " into DB.")
	return 
	


def print_all_items(table):
	print(table.scan())