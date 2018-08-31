import sys

from config import LINES_PER_LAMBDA, s3_client
from itertools import zip_longest

'''
Takes a file and subdivides it into chunks that we can process in a single Lambda function

'''


def process_file_to_smaller(file):

	'''
	Takes a file and breaks it up into smaller chunks so it can fit into Lambda 5 minute limit for running a process


	Code taken from 
	https://stackoverflow.com/questions/16289859/splitting-large-text-file-into-smaller-text-files-by-line-numbers-using-python
	'''

	print("Breaking up data into smaller files...")

	def grouper(n, iterable, fill_value = None):
		args = [iter(iterable)] * n
		return zip_longest(fillvalue = fill_value, *args)

	with open(file) as f:
		for i, g in enumerate(grouper(LINES_PER_LAMBDA, f, fill_value = ''), 1):
			with open('app_lambda_file_{0}.txt'.format(i * LINES_PER_LAMBDA), 'w') as fout:
				fout.writelines(g)
		f.close()
		
	print("Done splitting data.")
	return

	
def s3_break_up_file(list_of_data, s3_bucket):
	'''
	Function to interact with splitting up an s3 object and then writing it into an s3 object instead of text files locally
	'''
	print("Breaking up data into smaller files...")

	for i in range(0, len(list_of_data), LINES_PER_LAMBDA):
		if i + LINES_PER_LAMBDA >= len(list_of_data):
			curr_chunk = list_of_data[i:]
		else:
			curr_chunk = list_of_data[i:i + LINES_PER_LAMBDA]
		curr_chunk_string = '\n'.join(curr_chunk)
		curr_chunk_bytes = curr_chunk_string.encode('utf-8')
		object_name = 'app_lambda_file_' + str(i) + '.txt'
		response = s3_client.put_object(Body = curr_chunk_bytes, Bucket = s3_bucket, Key = object_name)

	print("Done creating smaller files.")
	return

def main(args):
	'''
	args[1] should be the data file location that we are accessing 

	'''
	process_file(args[1])


if __name__ == "__main__":
	main(sys.argv)