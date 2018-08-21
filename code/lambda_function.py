'''
These are the handlers that will be used by AWS whenever there is a trigger

'''


def file_download_lambda_handler(event, context):
	'''
	event is in the form of dict that passes event data to handler
	context is of type LambdaContext, contains runtime information

	Documentation: https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
	'''

	return None


def file_split_lambda_handler(event, context):

	pass

def process_into_dynamo_lambda_handler(event, context):

	pass