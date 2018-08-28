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

from config import lmbda_client, \
					S3_BUCKET_NAME, \
					FILE_DOWNLOAD_FUNCTION_NAME, \
					FILE_SPLIT_FUNCTION_NAME, \
					FILE_PROCESS_FUNCTION_NAME, \
					LAMBDA_ROLE, \
					HANDLER_MODULE_NAME

def create_file_download_lambda_function():

	#documentation at https://boto3.readthedocs.io/en/latest/reference/services/lambda.html#Lambda.Client.create_function
	response = lmbda_client.create_function(
		FunctionName = FILE_DOWNLOAD_FUNCTION_NAME,
		Runtime = 'python3.6',
		Role = LAMBDA_ROLE,
		Handler = HANDLER_MODULE_NAME + '.' + 'file_download_lambda_handler', #should match the function name of corresponding lambda handler function below
		Code = {
			#'ZipFile': b'bytes',
			'S3Bucket': S3_BUCKET_NAME,
			#'S3Key': 'string',
			#'S3ObjectVersion': 'string'
			#unsure if commented parameters are needed, need to look into more
		},
		Description = 'Downloads app data into S3 bucket periodically for ads.txt searching.',
		Timeout = 300, #optional but documentation recommends setting this
		# MemorySize = #optional but may put in later
	)
	pass


def create_file_split_lambda_function():
	response = lmbda_client.create_function(
		FunctionName = FILE_SPLIT_FUNCTION_NAME,
		Runtime = 'python3.6',
		Role = LAMBDA_ROLE,
		Handler = HANDLER_MODULE_NAME + '.' + 'file_split_lambda_handler',
		Code = {
			#'ZipFile': b'bytes',
			'S3Bucket': S3_BUCKET_NAME,
			#'S3Key': 'string',
			#'S3ObjectVersion': 'string'
			#unsure if commented parameters are needed, need to look into more
		},
		Description = 'Splits large data file into smaller files in S3 bucket.',
		Timeout = 300
	)

	pass


def create_file_process_into_dynamo_lambda_function():
	response = lmbda_client.create_function(
		FunctionName = FILE_PROCESS_FUNCTION_NAME,
		Runtime = 'python3.6',
		Role = LAMBDA_ROLE,
		Handler = HANDLER_MODULE_NAME + '.' + 'process_into_dynamo_lambda_handler',
		Code = {
			#'ZipFile': b'bytes',
			'S3Bucket': S3_BUCKET_NAME,
			#'S3Key': 'string',
			#'S3ObjectVersion': 'string'
			#unsure if commented parameters are needed, need to look into more		
		},
		Description = 'Processes file into DynamoDB table.',
		Timeout = 300

	)
	pass





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
	data_location = event['data_location']
	download_data(data_location)
	return


def file_split_lambda_handler(event, context):
	'''
	This handler will execute upon the dump being downloaded. It takes the giant
	file and splits it into smaller files that can each be processed separately.

	event should at least have:
	file_name - file that we are splitting into smaller chunks
	smaller_file_name_format - some indication of how the smaller files will be structured
	'''

	data_file = event['data_file']
	process_file_to_smaller(data_file)
	return
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
	small_data_file = event['lambda_data_file']
	process_file_into_dynamo(small_data_file)
	pass