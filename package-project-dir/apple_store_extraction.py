'''
Code to be written for extracting ads.txt location from ios apps.
Function prototypes written here modeled after google_playstore_extraction.py
Waiting to receive sample apple store data file to write these functions.



Notes:
sellerUrl in sample file seems probably be where we'll build our url from (website in playstore file)
budleId also seems important (package name in playstore file)
artistpreviewurl is the same as market url? (unsure), could also be trackViewUrl


'''


import re
import sys
from check_url import *
from utils import *


def look_for_ads_txt_url(entry_line):

	def check_description_in_metadata():
		'''
		Check the description property of the metadata for a URL 
		with an ads.txt scheme defined. e.g., 
		"adstxt://zynga.com/wordswithfriends/ads.txt". 
		If a valid ads.txt file exists, use it.
	

		'''
		ads_txt_regex = r'(adstx.+?/ads.txt)'
		if 'ads.txt' in entry_line:
			find_ads_txt = re.search(ads_txt_regex, entry_line, re.IGNORECASE)
			if find_ads_txt:
				return find_ads_txt[0]

		return ''


	def check_entry_site_ads_txt_url():
		'''
		Entire site entry + ads.txt. If the site entry is 
		"http://www.zynga.com/wordswithfriends" then look in 
		"http://www.zynga.com/wordswithfriends/ads.txt" for a 
		valid ads.txt file. If a valid ads.txt file exists, use it. 
		(skip further steps)

		'''

		site_entry_marker = 'sellerUrl'
		site_entry = parse_for_specific_parameter(site_entry_marker, entry_line)[0]
		site_entry = check_missing_slash(site_entry)
		possible_url = site_entry + 'ads.txt'

		pass

	def check_full_domain_url():
		pass


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
	pass
