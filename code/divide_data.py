import tarfile
import time
from datetime import datetime

from config import LINES_PER_LAMBDA, BREAK_UP_TIME_LIMIT

from clients import s3_client, data_s3_client
from itertools import zip_longest
from direct_write import s3_determine_app_store

"""
Takes a file and subdivides it into chunks that we can process in a single Lambda function

"""

def find_most_recent_object(bucket, prefix):
	"""
	looks into an s3 bucket and finds the most recently modified object
	"""

	all_objects = data_s3_client.list_objects(Bucket = bucket, Prefix = prefix)
	most_recent_key = ''
	most_recent_datetime = datetime(2000, 1, 1) #arbitrarily set to very early date
	for obj in all_objects['Contents']:
		if obj['LastModified'].timestamp() > most_recent_datetime.timestamp():
			most_recent_key = obj['Key']
			most_recent_datetime = obj['LastModified']
	print('Most recent object is ', most_recent_key)
	return most_recent_key


	
def s3_break_up_file(data, s3_bucket, start_line_number = 0):
	"""
	Function to interact with splitting up an s3 object 
	and then writing it into an s3 object instead of text files locally.
	"""

	def put_into_s3(chunk, app_store, line_number):
		chunk_bytes = b''.join(chunk)
		object_name = 'adstxt/app_lambda_file_' + app_store +'_' + str(line_number) + '.txt'
		try:
			response = s3_client.put_object(
				Body = chunk_bytes, 
				Bucket = s3_bucket, 
				Key = object_name)
		except Exception as e:
			print(e)
			print('Unable to write ' + object_name + ' to s3. Skipping.')



	print('Breaking up data into smaller files...')

	start_time = time.time()

	tar = tarfile.open(mode = 'r|*', fileobj = data)

	app_store = ''
	curr_chunk = []
	for entry in tar:
		file_obj = tar.extractfile(entry)
		line_number = 0
		for line in file_obj:
			line_number += 1
			if line_number < start_line_number:
				continue
			if app_store == '':
				app_store = s3_determine_app_store(line.decode())
			curr_chunk.append(line)
			if len(curr_chunk) == LINES_PER_LAMBDA:
				put_into_s3(curr_chunk, app_store, line_number)
				curr_chunk = []

			if time.time() - start_time > BREAK_UP_TIME_LIMIT and len(curr_chunk) > 0: 
				#process this chunk into a text file
				put_into_s3(curr_chunk, app_store, line_number)
				#return the line_number to start the next one at
				return line_number

	#check if there's an incomplete chunk near end and if so, we want to process that too
	if len(curr_chunk) > 0:
		put_into_s3(curr_chunk, app_store, line_number)

	print('Done creating smaller files.')
	return 0 #to keep consistent with what type we return
