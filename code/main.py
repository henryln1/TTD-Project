from check_url import *
from merge_results import *
#import google_playstore_extraction as google
from utils import *
import sys
import time

from extractor import *
from config import *
from write_to_dynamo import *
from query_dynamo import *

def construct_csv_file_location(app_store):
	return app_store_to_csv_dict[app_store]


def determine_app_store(file_name):
	google_play_string = 'https://play.google.com/store'


	#dummy strings for now until we get Apple/Tencent data
	apple_ios_string = 'http://itunes.apple.com'
	tencent_string = 'https://tencent.com/store'


	#we just need to check the first line assuming one data file only contains info from one app store
	with open(file_name, 'r', encoding = 'utf-8') as f:
		first_line = f.readline()
		if google_play_string in first_line:
			return 'Google'
		if apple_ios_string in first_line:
			return 'Apple'
		if tencent_string in first_line:
			return 'Tencent'

	print("Please examine your data file. No valid app store detected.")
	print("Exiting...")
	exit()
	return ''




'''
Notes: Could improve flexibility of argument intake if we swapped to regexes to extract the information given by the command. 
	Not very urgent however, can improve later on when everything else is completed and there is extra time.

'''

def main(args):

	if len(args) == 1:
		print("No arguments provided. Please execute: \"python main.py --help\" for instructions. ")
		return
	if args[1] == '--help':
		print('''
			This program takes a file with metadata information 
			about apps and generates a csv file that maps app id to 
			ads.txt location. The basic requirement is a data file 
			where each line contains info about an app. Optional parameters 
			follow the data file location and are separated by spaces.
			** denotes a mandatory input.
			<> denotes an optional input.

			python main.py *data file* <app store name> <csv_file>

			Example:
			python main.py dummy_data.txt Apple output.csv
			''')
		return

	start_time = time.time()

	file_path = args[1]
	app_store = ''
	csv_file_location = ''
	if len(args) == 2: #no app store provided
		app_store = determine_app_store(file_path)
	else:
		app_store = args[2]

	app_id_marker, market_url_marker, seller_url, package = store_keywords_dict[app_store]

	extractor = Extractor(seller_url, package)

	assert app_store in possible_app_stores
	file_path = args[1]
	if validate_file(file_path) is False:
		print("Unable to find data file. Please check your command and rerun.")
		return
	app_ids_to_location_dict = open_file_create_dict(file_path, app_id_marker, market_url_marker, extractor)
	change_set = create_change_list(app_ids_to_location_dict)
	#TODO need to write to different csv file depending on which app store the data comes from

	if len(args) == 4: #csv file is given
		csv_file_location = args[3]
	else:
		csv_file_location = construct_csv_file_location(app_store)

	try:
		merge_into_file(csv_file_location, change_set)
	except Exception as e:
		print(e)
		print("Unable to merge changes into csv file. Exiting. Please try again.")
		return
	process_csv_file(csv_file_location)
	# try:
	# 	process_csv_file(csv_file_location)
	# except Exception as e:
	# 	print(e)
	# 	print("Unable to process csv file into DB. Exiting.")

	print("Processing file took ", time.time() - start_time, " seconds.")




if __name__ == "__main__":
	'''
	Executes following code when you run "python main.py" in command line
	Takes in multiple arguments/flags

	arg1 should be the data file
	arg2 should be the app store where the data is coming from.
	arg3 should be the output csv file path
	'''

	main(sys.argv)




