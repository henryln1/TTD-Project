import requests
import re

'''
File contains code to look at an url and determine whether or not there is a text file present

'''


def extensive_check_for_ads_txt(request):
	'''
	After performing the initial status code check, we now need to check for soft 404s and other problematic things
	to verify whether or not there is a ads.txt file present.

	'''

	def check_for_valid_ads_txt_entries(content):

		'''
		needs to look at the contents of the webpage to see if it actually contains valid ads.txt entries

		UPDATE: does not look like this function is needed. 
		'''
		valid_ads_txt_entry_regex = r'.+?, .*?, (DIRECT)|(RESELLER)'
		if 'html' not in content and re.search(valid_ads_txt_entry_regex, content, re.IGNORECASE):
			return True
		return False

	content = request.text
	if (not (
		'<!DOCTYPE' in content or 
		'<!doctype' in content or 
		'<html' in content or 
		'<HTML' in content or 
		'<content:encoded' in content) 
	and
		('DIRECT' in content or 
		'RESELLER' in content or 
		'direct' in content or 
		'reseller' in content)):
	#and (not re.search('Page not found', content, re.IGNORECASE))):
	#and (check_for_valid_ads_txt_entries(content))):
		return True


	return False


def check_valid_url_ad_txt(url_path):
	'''
	Given a url, we try to check if it is valid. Returns a boolean 
	'''

	'''
	try/except is to handle the errors when the website crashes the process. 
	'''


	request = None

	'''
	Tested timeout limits of 1-5 seconds and it seems that 3 is a good number to stick to for now.
	'''
	
	try:
		request = requests.get(url_path, timeout = 3)
	except:
		#print("Request timed out for " + url_path + ".")
		print("Error encountered pinging " + url_path + ". Defaulting to no ads.txt here.")
		return False

	if request.status_code == 200:
		return extensive_check_for_ads_txt(request)
	return False


def extract_url_contents(url_list):
	'''
	Takes a list of urls (valid and invalid for now) and returns the dict structured as:

	url : url_contents

	'''
	url_contents_dict = {}
	for url in url_list:
		if check_valid_url_ad_txt(url):
			url_contents_dict[url] = request.get(url_path).text
		else:
			url_contents_dict[url] = None
	return url_contents_dict