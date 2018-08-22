'''
These are the handlers that will be used by AWS whenever there is a trigger
From my current understanding, a trigger will execute the corresponding
function whenever it occurs, so I just need to put what code I want to run
in corresponding handler
'''

#used in 1st lambda handler
from pull_data import download_data

#used in 2nd lambda handler
from divide_data import process_file_to_smaller

#used in 3rd lambda handler
from direct_write import process_file_into_dynamo


def file_download_lambda_handler(event, context):
	'''
	event is in the form of dict that passes event data to handler
	context is of type LambdaContext, contains runtime information

	Documentation: https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
	'''

	'''
	This handler should be on a scheduled trigger, occurrly either daily or weekly.
	It should then download the data dump from 42matters.

	event should at least have:
	42matters file location
	possible username/password to download data?

	'''

	return None


def file_split_lambda_handler(event, context):
	'''
	This handler will execute upon the dump being downloaded. It takes the giant
	file and splits it into smaller files that can each be processed separately.

	event should at least have:
	file_name - file that we are splitting into smaller chunks
	smaller_file_name_format - some indication of how the smaller files will be structured
	'''

	pass

def process_into_dynamo_lambda_handler(event, context):
	'''
	Triggers whenever a smaller file is occurred (from the above handler) and
	runs url extraction and then writes that information into amazon dynamodb.
	Since this triggers whenever a smaller file is created, there will be many of these
	running concurrently, not in sequential order. 

	event should at least have:
	file_name - file that we are processing 

	'''

	pass