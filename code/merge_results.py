from utils import *
#from parse_ads_txt_location import *
import re
import pandas as pd
from check_url import *
import os
import os.path
import numpy as np
from config import *


'''
After checking the URLs for validity of a text file, we want to take the information 
and process it into our giant text file. Tentatively thinking that this set of functions
will rely upon a dictionary from ad_text_url to ad_text_url_content.

Need to figure out how to merge results into whatever text/csv file we have. 

'''



def create_change_list(app_ids_to_location_dict):
	changes = []
	for app in app_ids_to_location_dict:
		if app_ids_to_location_dict[app] == '':
			changes.append((app, 'NONE'))
		else:
			changes.append((app, app_ids_to_location_dict[app]))
	return changes



def merge_into_file(file_name, list_of_changes):
	'''
	file_name: output file location
	list_of_changes: list of changes generated by process_scan_results that we will step through and make in the file
		Structured as:
			[(app id, urls or NONE), ..]
		
	'''

	def check_existing_app_id(app_id_name, dataframe):
		'''
		Checks if the csv file already contains the current app_id
		'''
		column_name = 'app_id'
		exists = dataframe[dataframe['app_id'] == app_id_name]
		if not exists.empty:
			print(str(app_id_name) + " already exists in csv file. Updating...")
		else:
			print(str(app_id_name) + " is a new entry. Adding...")
		return not exists.empty


	def modify_existing_csv():
		'''
		there's already a csv file present so we just need to update it.
		'''
		csv_dataframe = pd.read_csv(file_name)

		new_additions = []
		for change in list_of_changes:
			current_app_id, ads_txt_location = change
			if ads_txt_location == 'NONE':
				ads_txt_location = 'No ads.txt found.'

			if check_existing_app_id(str(current_app_id), csv_dataframe): #app id already exists, so we have to update that row 
				#looks for existing row and updates ads.txt location
				app_id_column = 'app_id'
				csv_dataframe.loc[csv_dataframe['app_id'] == str(current_app_id), 'ads.txt_location'] = ads_txt_location
			else: #adding a new entry to csv table
				new_additions.append((str(current_app_id), ads_txt_location))
		new_entries_dataframe = create_new_csv(new_additions)
		csv_dataframe = csv_dataframe.append(new_entries_dataframe)

		return csv_dataframe


	def create_new_csv(changes):
		'''
		No csv file so we have to create it from current info.
		'''
		max_length = 50
		for change_index in range(len(changes)):
			app_id, location = changes[change_index]
			if location == 'NONE':
				changes[change_index] = (app_id, 'No ads.txt found.')

		column_names = ['app_id', 'ads.txt_location']
		new_csv_dataframe = pd.DataFrame(changes, columns = column_names)
		return new_csv_dataframe
		


	if validate_file(file_name):
		print("Found existing csv file, modifying...")
		#open file and modify it
		csv_dataframe = modify_existing_csv()
	else: 
		print("No csv file found. Creating new csv file...")
		#no existing file so creating a new one
		csv_dataframe = create_new_csv(list_of_changes)
	
	#saving a csv file now
	csv_dataframe.to_csv(file_name, index = False)
	print("CSV file complete. File updated with latest information from data.")
	return




