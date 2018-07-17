from check_url import *
from merge_results import *
from parse_ads_txt_location import *
from utils import *
import pandas as pd
import time
import os

'''
Contains tests written to make sure all the functions written 
are performing as expected.
'''


def check_url_tests():
	example_valid_url = 'http://www.google.com/chrome/android/com.android.chrome/ads.txt'
	example_fake_url = 'http://slither.io/air.com.hypah.io.slither/ads.txt'
	valid_url_check = check_valid_url_ad_txt(example_valid_url)
	assert valid_url_check is True
	fake_url_check = check_valid_url_ad_txt(example_fake_url)
	assert fake_url_check is False

	return

def check_utils_tests():

	example_list = ['A', 'B', 'C', 'D', 'A', 'B']
	removed_duplicates = remove_duplicates_from_list(example_list)
	assert len(removed_duplicates) == 4

	return

def check_parse_ads_txt_location_tests():
	small_data_file_name = '../dummy_data/playstore-00'
	lines = open_file(small_data_file_name)
	assert len(lines) == 100 #check all lines are being loaded
	assert """air.com.hypah.io.slither", "short_desc": "Play online with people all over the world! Can YOU become the longest player?""" in lines[0] #check first entry to make sure it's right
	test_url = create_single_txt_location(lines[0])
	assert test_url == 'http://slither.io/air.com.hypah.io.slither/ads.txt'

	return


def check_merge_results_tests():


	file_name = '../test_merge.csv' #test file program creates
	correct_check_file_name = '../correct_output_test.csv' #file to compare against for first check
	fully_completed_file_check = '../correct_output_test_complete_merge.csv' #file to compare against for second check

	#checking if test file already exists (leftover from past test run). If it does, we delete it
	if os.path.isfile(file_name) and os.access(file_name, os.R_OK):
		os.remove(file_name)


	#test for when we create a new csv file
	dummy_ids_to_urls_dict = {
		'fruit_ninja': ['http://fruitninja.com/ads.txt', 'http://fruitninja.com/apps/ads.txt'],
		'google_translate': ['http://google.com/ads.txt'],
		'angry_birds': []
	}
	changes = create_change_list(dummy_ids_to_urls_dict)
	assert ('fruit_ninja', 'NONE') in changes
	assert('google_translate', 'NONE') in changes
	assert('angry_birds', 'NONE') in changes
	assert len(changes) == 3
	merge_into_file(file_name, changes)
	#file created, now time to load it and check if it is accurate
	data_entries = pd.read_csv(file_name)
	expected_array = pd.read_csv(correct_check_file_name)
	assert data_entries.equals(expected_array)



	#time to check if it works when modifying the file
	new_dummy_ids_to_url_dict = {
		'google': ['http://www.google.com/chrome/android/com.android.chrome/ads.txt'], #adding new entry to current file
		'google_translate': ['http://www.google.com/chrome/android/com.android.chrome/ads.txt'] #test to update a current entry
	}
	changes = create_change_list(new_dummy_ids_to_url_dict)
	merge_into_file(file_name, changes)
	full_expected_array = pd.read_csv(fully_completed_file_check)
	modified_data_entries = pd.read_csv(file_name)
	assert modified_data_entries.equals(full_expected_array)

	return 



def run_all_tests():
	#If the tests start taking a sizeable amount of time, add flags so tests can be run individually or in smaller groups - not needed currently.
	print("Executing all tests.")
	start_time = time.time()
	check_url_tests()
	print("url tests passed.")
	check_utils_tests()
	print("utils tests passed.")
	check_parse_ads_txt_location_tests()
	print("locations tests passed.")
	check_merge_results_tests()
	print("merge tests passed.")
	print("All tests run. Time Elapsed: %s seconds. Program stopping. " % (time.time() - start_time))

	#deleting created csv file
	os.remove('../test_merge.csv')

def main():
	run_all_tests()



if __name__ == "__main__":

	main()