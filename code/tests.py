from check_url import *
from merge_results import *
from parse_ads_txt_location import *
from utils import *
import pandas as pd

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
	removed_duplicates = removed_duplicates_from_list(example_list)
	assert len(removed_duplicates) == 4

def check_parse_ads_txt_location_tests():
	pass


def check_merge_results_tests():
	dummy_ids_to_urls_dict = {
		'fruit_ninja': ['fruitninja.com/ads.txt', 'fruitninja.com/apps/ads.txt'],
		'google_translate': ['google.com/ads.txt'],
		'angry_birds': []
	}
	changes = create_change_list(dummy_ids_to_urls_dict)
	assert ('fruit_ninja', ('fruitninja.com/ads.txt', 'fruitninja.com/apps/ads.txt')) in changes
	assert('google_translate', ('google.com/ads.txt')) in changes
	assert('angry_birds', 'NONE') in changes
	assert len(changes) == 3

	file_name = '../test_merge.csv'
	merge_into_file(file_name, changes)
	#file created, now time to load it and check if it is accurate

	data_entries = pd.read_csv(file_name)
	data_entries_array = data_entries.as_matrix()
	expected_array = [['fruit_ninja', ('fruitninja.com/ads.txt', 'fruitninja.com/apps/ads.txt')], 
					['google_translate', ('google.com/ads.txt')],
					['angry_birds', 'No ads.txt found']]

	assert data_entries_array == np.asarray(expected_array)

	#time to check if it works when modifying the file
	new_dummy_ids_to_url_dict = {
		'flappy_bird': ['flappybird.com/ads.txt']
	}

	changes = create_change_list(new_dummy_ids_to_url_dict)
	merge_into_file(file_name, changes)
	expected_array.append(['flappy_bird', ('flappybird.com/ads.txt')])

	modified_data_entries = pd.read_csv(file_name)
	modified_data_entries_array = modified_data_entries.as_matrix()
	assert modified_data_entries_array == np.as_array(expected_array)
	return 


