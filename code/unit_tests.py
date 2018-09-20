import unittest

from utils import remove_duplicates_from_list
from check_url import check_valid_url_ad_txt
from write_to_dynamo import find_table, \
						add_item_to_table, \
						update_item, \
						delete_item, \
						retrieve_item, \
						key_exists

from query_dynamo import scan_ads_txt_location

class test_url_methods(unittest.TestCase):

	def test_valid_url(self):
		example_valid_url = 'http://slither.io/ads.txt'
		valid_url_check = check_valid_url_ad_txt(example_valid_url)
		self.assertTrue(valid_url_check)

	def test_invalid_url(self):
		example_fake_url = 'http://slither.io/air.com.hypah.io.slither/ads.txt'
		fake_url_check = check_valid_url_ad_txt(example_fake_url)
		self.assertFalse(fake_url_check)


class test_utils_methods(unittest.TestCase):

	def test_remove_duplicates(self):
		example_list = ['A', 'B', 'C', 'D', 'A', 'B']
		removed_duplicates = remove_duplicates_from_list(example_list)
		self.assertEqual(len(removed_duplicates), 4)

class test_dynamo_methods(unittest.TestCase):

	def test_single_item_write_and_query_dynamo(self):
		#should have one assert per test, keep in mind
		table = find_table('apple')
		item = {
			'App_ID': "('eBay Inc.', 'http://itunes.apple.com/artist/ebay-inc/id282614219?uo=5')",
			'FileLocation': 'No ads.txt found.'
		}
		key = item['App_ID']
		value = item['FileLocation']
		add_item_to_table(table, key, value)
		self.assertEqual(len(scan_ads_txt_location(table, key)), 1)

		key_dict_form = {
			'App_ID': key
		}
		retrieved_item = retrieve_item(table, key_dict_form)
		self.assertEqual(item, retrieved_item)
		values_to_update_dict_form = {
			':l': 'No ads.txt found modified.'
		}
		update_item(table, key_dict_form, values_to_update_dict_form)
		delete_item(table, key_dict_form)	
		self.assertFalse(key_exists(key, table))
		


if __name__ == '__main__':
	unittest.main()