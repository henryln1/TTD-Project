import sys

from config import LINES_PER_LAMBDA, s3_client
from itertools import zip_longest

'''
Takes a file and subdivides it into chunks that we can process in a single Lambda function

'''
	
def s3_break_up_file(data, s3_bucket):
	'''
	Function to interact with splitting up an s3 object and then writing it into an s3 object instead of text files locally
	'''
	print("Breaking up data into smaller files...")

	data_iterator = data.iter_lines()

	curr_chunk = []
	chunk_number = 0
	count = 0
	for line in data_iterator:
		curr_chunk.append(line)
		if count == LINES_PER_LAMBDA:
			curr_chunk_string = ''.join(curr_chunk)
			curr_chunk_bytes = curr_chunk_string.encode('utf-8')
			object_name = 'app_lambda_file_' + str(chunk_number * count) + '.txt'
			response = s3_client.put_object(Body = curr_chunk_bytes, Bucket = s3_bucket, Key = object_name)

			#reset chunk
			curr_chunk = []
			#reset count
			count = 0
			#increase chunk number
			chunk_number += 1
		else:
			count += 1

	#check if there's an incomplete chunk near end and if so, we want to process that too
	if curr_chunk:
		curr_chunk_string = ''.join(curr_chunk)
		curr_chunk_bytes = curr_chunk_string.encode('utf-8')
		object_name = 'app_lambda_file_' + str(chunk_number * count) + '.txt'
		response = s3_client.put_object(Body = curr_chunk_bytes, Bucket = s3_bucket, Key = object_name)



	# for i in range(0, len(list_of_data), LINES_PER_LAMBDA):
	# 	if i + LINES_PER_LAMBDA >= len(list_of_data):
	# 		curr_chunk = list_of_data[i:]
	# 	else:
	# 		curr_chunk = list_of_data[i:i + LINES_PER_LAMBDA]
	# 	curr_chunk_string = '\n'.join(curr_chunk)
	# 	curr_chunk_bytes = curr_chunk_string.encode('utf-8')
	# 	object_name = 'app_lambda_file_' + str(i) + '.txt'
	# 	response = s3_client.put_object(Body = curr_chunk_bytes, Bucket = s3_bucket, Key = object_name)

	print("Done creating smaller files.")
	return
