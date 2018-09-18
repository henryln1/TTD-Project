import time

from config import MAX_BATCH_SIZE, \
					APPLE_STORE_TABLE_NAME, \
					GOOGLE_PLAY_TABLE_NAME, \
					TABLE_READ_CAPACITY, \
					TABLE_WRITE_CAPACITY

from clients import dynamodb_resource, dynamodb_client


from query_dynamo import scan_ads_txt_location
from utils import write_exception_to_file


"""
parition key helps distribute data evenly, choose something that has a large range of values 
sort key can help sort additionally with the partition key
"""


def create_new_table(table_name, primary_keys = None):
	start_time = time.time()
	if not primary_keys:
		#default to two colum table of app_id and ads.txt location
		table = dynamodb_resource.create_table(
			TableName = table_name,
			KeySchema = [
				{
					'AttributeName': 'App_ID',
					'KeyType': 'HASH' #Partition Key
				}
			],
			AttributeDefinitions = [
				{
					'AttributeName': 'App_ID',
					'AttributeType': 'S'

				}
			],
			ProvisionedThroughput = {
				'ReadCapacityUnits': TABLE_READ_CAPACITY,
				'WriteCapacityUnits': TABLE_WRITE_CAPACITY
			}
		)
	else:
		"""
		For the scenario when we have other keys identified other than the basic standard
		"""
		pass

	table.meta.client.get_waiter('table_exists').wait(TableName = table_name)
	print('Table took ', time.time() - start_time, ' seconds to create.')
	return table


def add_item_to_table(table, key, value):
	"""
	Table is a DynamoDB table
	item_information is a dict form from key to value that we add to the table
	"""

	item_information = {
		'App_ID': key,
		'FileLocation': value
	}
	try: 
		table.put_item(Item = item_information)
	except Exception as e:
		error_info = 'Unable to insert into table. Skipping ' + str(key) + ' with value: ' + str(value)
		print(error_info)
		print(e)


def retrieve_item(table, keys):

	"""
	table is a DynamoDB table
	keys is the information in dict form used to retrieve the item
	"""

	try:
		response = table.get_item(Key = keys)
		item = response['Item']
		return item
	except:
		print('Unable to retrieve ' + keys + '. The entry may not exist.')
		return None

def update_item(table, keys, values):
	"""
	table: db table
	keys: how to access item
	values: values to update
	"""

	key_dict_form = {
		'App_ID': keys
	}
	values_dict_form = {
		':val1': values
	}

	try:
		response = table.update_item(
			Key = key_dict_form,
			UpdateExpression = 'set FileLocation = :val1',
			ExpressionAttributeValues = values_dict_form)
	except Exception as e:
		error_info = 'Unable to update table. Skipping ' + str(keys) + ' with value: ' + str(values)
		print(error_info)
		print(e)


def delete_item(table, keys):
	"""
	deletes an item from given table using keys.
	NOTE: deleting the item does not remove the key from the table, so you can
	still access this key without it causing an error. It will just return an empty list or nothing.
	"""

	try:
		table.delete_item(Key = keys)
	except:
		print('Unable to delete item.')


def find_table(app_store):
	"""
	from the file name, we determine which table we are modifying with the changes
	"""

	if app_store == 'Google':
		table_name = GOOGLE_PLAY_TABLE_NAME
	elif app_store == 'Apple':
		table_name = APPLE_STORE_TABLE_NAME	
	else:
		print('Unable to determine which table.')
		print('Exiting.')
		return
	try:
		table = dynamodb_client.describe_table(TableName = table_name)
		table = dynamodb_resource.Table(table_name)
	#make this exception more specific
	except:
		print('No table found. Creating new table...')
		table = create_new_table(table_name)

	return table

def key_exists(keys, table):
	"""
	check if the app id is already present in the table
	"""

	items = scan_ads_txt_location(table, keys)
	if len(items) > 0:
		return True
	return False


def write_items_batch(items, table):
	"""
	uses built in batch writer to help speed up writing large number of items
	items is a list of items we want to write, already in correct format and 
	not exceeding max batch size
	"""

	assert len(items) <= MAX_BATCH_SIZE
	
	"""
	removes duplicate entries automatically before sending to Dynamo
	"""

	try:
		with table.batch_writer(overwrite_by_pkeys = ['App_ID']) as batch:
			for item in items:
				batch.put_item(Item = item)
	except Exception as e:
		print(e)



def print_all_items(table):
	print(table.scan())