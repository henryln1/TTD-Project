import re
import sys
from check_url import *
from utils import *



def look_for_ads_txt_url(entry_line):


	'''
	returns either a valid ads.txt location or an empty string ''

	'''

	def check_description_in_metadata():
		'''
		Check the description property of the metadata for a URL 
		with an ads.txt scheme defined. e.g., 
		"adstxt://zynga.com/wordswithfriends/ads.txt". 
		If a valid ads.txt file exists, use it.
	
		'''
		ads_txt_regex = r' (http.+?/ads.txt)'

		if 'ads.txt' in entry_line:
			#TODO, just a placeholder returning the entire line when ads.txt is found here. Will update with actual regex once I know format
			return entry_line

		return ''


	def check_entry_site_ads_txt_url():
		'''
		Entire site entry + ads.txt. If the site entry is 
		"http://www.zynga.com/wordswithfriends" then look in 
		"http://www.zynga.com/wordswithfriends/ads.txt" for a 
		valid ads.txt file. If a valid ads.txt file exists, use it. 
		(skip further steps)

		'''
		site_entry_marker = 'website'
		site_entry = parse_for_specific_parameter(site_entry_marker, entry_line)[0]
		site_entry = check_missing_slash(site_entry)
		possible_url = site_entry + 'ads.txt'

		if check_valid_url_ad_txt(possible_url):
			return possible_url
		return ''
		

	def check_full_domain_url():
		'''
		If we don't find an ads.txt file there, then revert to 
		checking for the file at "http://{topleveldomain+1}/{appId}/ads.txt". 
		For the example above, we would look at 
		http://zynga.com/com.zynga.words3/ads.txt to see if there is 
		a valid ads.txt file.
		'''

		site_entry_marker = 'website'
		site_entry = parse_for_specific_parameter(site_entry_marker, entry_line)[0]
		site_entry = check_missing_slash(site_entry)
		package_marker = 'package_name'
		package = parse_for_specific_parameter(package_marker, entry_line)[0]
		package = check_missing_slash(package)
		possible_url = site_entry + package + 'ads.txt'
		if check_valid_url_ad_txt(possible_url):
			return possible_url
		return ''
		

	
	'''
	all functions will either return a valid url or an empty string.
	We can use this format to then determine if we need to keep looking

	'''

	possible_url = ''

	#1
	possible_url = check_description_in_metadata()
	if possible_url != '':
		return possible_url

	#2
	possible_url = check_entry_site_ads_txt_url()
	if possible_url != '':
		return possible_url

	#3
	possible_url = check_full_domain_url()
	return possible_url


def open_file_create_dict(file_path):
	'''
	Opens up the data file and starts processing the data into a dictionary with format

	(app id, market url): ads.txt location

	'''
	ads_txt_location_dict = {}

	with open(file_path, 'r', encoding = 'utf-8') as f:
		current_entry = f.readline()

		while current_entry:
			app_id = parse_for_specific_parameter('title', current_entry)[0]
			market_url = parse_for_specific_parameter('market_url', current_entry)[0]
			if not app_id:
				print("Could not find title of app. Please investigate.")
			if not market_url:
				print("Could not find market url of app. Please investigate.")
			if app_id and market_url:
				ads_txt_location_dict[(app_id, market_url)] = look_for_ads_txt_url(current_entry)

			current_entry = f.readline()
		f.close()
	print(ads_txt_location_dict.values())
	return ads_txt_location_dict

















