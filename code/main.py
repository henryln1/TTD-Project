from check_url import *
from merge_results import *
from parse_ads_txt_location import *
from utils import *

possible_app_stores = ['Apple', 'Google', 'Tencent']



def construct_csv_file_location():
	pass



def determine_app_store(file_name):
	pass



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

			python main.py <data file> <app store name>

			Example:
			python main.py dummy_data.txt Apple
			''')
		return

	file_path = args[1]
	app_store = ''
	if len(args) == 2:
		app_store = determine_app_store(file_path)
	else:
		app_store = args[2]
	assert app_store in possible_app_stores
	file_path = args[1]
	if validate_file(file_path) is False:
		print("Unable to find data file. Please check parameter and rerun.")
		return
	app_ids_to_location_dict = open_file_create_dict(file_path)
	change_set = create_change_list(app_ids_to_location_dict)
	#TODO need to write to different csv file depending on which app store the data comes from
	csv_file_location = construct_csv_file_location(app_store)
	merge_into_file(csv_file_location, change_set)





if __name__ == "__main__":
	'''
	Executes following code when you run "python main.py" in command line
	Takes in multiple arguments/flags

	arg1 should be the data file
	arg2 should be the app store where the data is coming from.
	'''

	main(sys.argv)




