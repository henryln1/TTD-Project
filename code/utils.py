import os
import time
import datetime

"""
Place to keep functions that may be generally useful in the future

"""

def remove_duplicates_from_list(list_):
	return list(set(list_))


def validate_file(file):
	"""
	Checks to make sure a file is valid and readable
	"""
	if os.path.isfile(file) and os.access(file, os.R_OK):
		return True
	return False


def write_exception_to_file(file_name, exception_info, information):

	"""
	Writes errors to a log file that can later be inspected to determine source of problem.
	"""

	ts = time.time()
	timestamp = datetime.datetime.now()
	with open(file_name, 'a') as f:
		f.write(timestamp + '\n')
		f.write(str(exception_info) + '\n')
		f.write(information + '\n')
		f.close()


def check_missing_slash(s):
	"""
	Adds a slash to end of string if there is not one there already and then returns new string
	"""
	return s if s.endswith('/') else s + '/'
