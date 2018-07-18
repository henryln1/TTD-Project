import re
import sys
from collections import defaultdict
from check_url import *
from utils import *
'''
The purpose of this file is to take in a file with a list of entries from the 
playstore, parse that information, and then return a list of urls to check 
whether or not the ads.txt file exists for each one.

'''



def parse_for_specific_parameter(parameter_name, search_string):
	'''
	Uses regexes to find a specific piece of information in the entry.

	'''
	#regex_pattern = r'market_url": "(.+?)",'
	regex_pattern = re.escape(parameter_name) + r'": "(.+?)"'
	parameter = re.findall(regex_pattern, search_string)
	return parameter

def create_single_txt_location(entry_line):
	'''
	Takes in a single entry line and returns a string url with the format:
	http://{root_doamin_of_website}/{package}/ads.txt
	Example:
	http://slither.io/air.com.hypah.io.slither/ads.txt

	'''

	website = parse_for_specific_parameter('website', entry_line)
	package = parse_for_specific_parameter('package_name', entry_line)

	if len(website) != 1 or len(package) != 1:
		print("Something went wrong in creating the url. Please investigate.")

	ad_txt_name = 'ads.txt'

	#inconsistent website url inclusion of / so this part helps piece them together
	if website[0][-1] != '/':
		website[0] += '/'
	if package[0][-1] != '/':
		package[0] += '/'
	return website[0] + package[0] + ad_txt_name

def open_file(file_path):
	
	with open(file_path, 'r', encoding = 'utf-8') as f:
		all_lines = f.readlines()
		all_lines = [line.rstrip('\n') for line in all_lines]
		f.close()
	return all_lines

def open_file_create_dict(file_path):
	'''
	Opens the file at the file path and goes through it line by line.
	For each line/entry, creates a dict from the market url to the location
	of the ads.txt file for that entry.
	Example:
		https://play.google.com/store/apps/details?id=air.com.hypah.io.slither
		: http://slither.io/air.com.hypah.io.slither/ads.txt

	'''


	all_lines = open_file(file_path)
	market_url_to_ads_txt_dict = defaultdict(str)

	#print(all_lines[0])
	for lineIndex in range(len(all_lines)):
		market_url = parse_for_specific_parameter('market_url', all_lines[lineIndex])
		#print("Entry " + str(lineIndex) + " " + "Market url: ", market_url[0])
		#complains when it can't find the market url. 
		if not market_url:
			print("Entry " + str(lineIndex) + " does not have a market url. Please investigate.")
		#complains when it finds too many.
		elif len(market_url) > 1:
			print("Entry " + str(lineIndex) + " found multiple market urls. Please investigate.")
		else:
			market_url_to_ads_txt_dict[market_url[0]] = create_single_txt_location(all_lines[lineIndex])


	return market_url_to_ads_txt_dict

def write_dict_to_new_file(file_name, dict_name):
	'''
	Writes a dictionary to new file, each line being a key/value pair

	'''

	with open(file_name, 'w') as f:
		for key in dict_name:
			f.write("Market Url: " + key + ", Ads Txt URL: " + dict_name[key] + "\n")

		f.close()

def write_urls_to_file(file_name, dict_name, check_validity = False, no_duplicates = False):
	'''
	writes only the urls to a text file
	'''

	urls = [dict_name[key] for key in dict_name]
	if no_duplicates:
		urls = remove_duplicates_from_list(urls)
	with open(file_name, 'w') as f:

		for urlIndex in range(len(urls)):
			print(urls[urlIndex])
			if not check_validity:
				f.write("Url " + str(urlIndex) + ": " + urls[urlIndex] + '\n')
			else:
				validity = check_valid_url_ad_txt(urls[urlIndex])
				f.write("Url " + str(urlIndex) + ": " + urls[urlIndex] + ' is ' + str(validity) + '\n')
		f.close()


def main(args):
	data_entries_file = args[1]
	market_url_to_ads_txt_dict = open_file_create_dict(data_entries_file)
	
	urls_only_txt_file_name = '../urls_validity.txt'
	write_dict_to_new_file('../parsed_out_urls.txt', market_url_to_ads_txt_dict)
	write_urls_to_file(urls_only_txt_file_name, market_url_to_ads_txt_dict, check_validity = True, no_duplicates = False)

	return
	#TODO


if __name__ == "__main__":
	'''
	Executes when running this file.
	sys args contains the arguments you pass in when running this file:
	file.py arg0 arg1 arg2

	arg1 should be a path to the data entries


	'''
	main(sys.argv)

