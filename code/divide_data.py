import sys
from config import *
from itertools import zip_longest

'''
Takes a file and subdivides it into chunks that we can process in a single Lambda function

'''


def process_file(file):

	'''
	Takes a file and breaks it up into smaller chunks so it can fit into Lambda 5 minute limit for running a process


	Code taken from 
	https://stackoverflow.com/questions/16289859/splitting-large-text-file-into-smaller-text-files-by-line-numbers-using-python
	'''


	def grouper(n, iterable, fill_value = None):
		args = [iter(iterable)] * n
		return zip_longest(fillvalue = fill_value, *args)

	with open(file) as f:
		for i, g in enumerate(grouper(LINES_PER_LAMBDA, f, fill_value = ''), 1):
			with open('lambda_small_file_{0}.txt'.format(i * LINES_PER_LAMBDA), 'w') as fout:
				fout.writelines(g)

	pass




def main(args):
	'''
	args[1] should be the data file location that we are accessing 

	'''
	process_file(args[1])


if __name__ == "__main__":
	main(sys.argv)