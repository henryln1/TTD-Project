import os
import re


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
	#regex_pattern = r'market_url": "(.+?)",'
	regex_pattern = re.escape(parameter_name) + r'": "(.+?)"'
	parameter = re.search(regex_pattern, search_string)
	#print("entire thing: ", parameter[0])
	#print("1st ", parameter[1])
	return parameter[1]


def check_missing_slash(string):
	'''
	Adds a slash to end of string if there is not one there already and then returns new string
	'''

	if string[-1] != '/':
		return string + '/'
	return string


def open_file(file_path):
	
	with open(file_path, 'r', encoding = 'utf-8') as f:
		all_lines = f.readlines()
		all_lines = [line.rstrip('\n') for line in all_lines]
		f.close()
	return all_lines