'''
Code to be written for extracting ads.txt location from ios apps.
Function prototypes written here modeled after google_playstore_extraction.py
Waiting to receive sample apple store data file to write these functions.

'''


import re
import sys
from check_url import *
from utils import *


def look_for_ads_txt_url(entry_line):

	def check_description_in_metadata():
		pass

	def check_entry_site_ads_txt_url():
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
