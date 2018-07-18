import os


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
