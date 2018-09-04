import os
import re
import time
import datetime

'''
Place to keep functions that may be generally useful in the future

'''

def remove_duplicates_from_list(list_):
	return list(set(list_))


def validate_file(file):
	'''
	Checks to make sure a file is valid and readable
	'''
	if os.path.isfile(file) and os.access(file, os.R_OK):
		return True
	return False



def parse_for_specific_parameter(parameter_name, search_string):
	'''
	Uses regexes to find a specific piece of information in the entry.

	'''
	regex_pattern = re.escape(parameter_name) + r'": "(.+?)"'
	parameter = re.search(regex_pattern, search_string)
	try:
		return parameter[1]
	except:
		return None

def write_exception_to_file(file_name, exception, information):

	'''
	Writes errors to a log file that can later be inspected to determine source of problem.
	'''

	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with open(file_name, 'a') as f:
		f.write(timestamp + '\n')
		f.write(str(exception) + '\n')
		f.write(information + '\n')
		f.close()
	return


def check_missing_slash(string):
	'''
	Adds a slash to end of string if there is not one there already and then returns new string
	'''
	if not string.endswith('/'):
		string += '/'
	return string
