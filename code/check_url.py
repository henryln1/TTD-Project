import requests

from config import NUMBER_ATTEMPTS

'''
File contains code to look at an url and determine whether or not there is a text file present

'''


def extensive_check_for_ads_txt(request):
	'''
	After performing the initial status code check, we now need to check for soft 404s and other problematic things
	to verify whether or not there is a ads.txt file present.
	'''

	retry_attempt_counter = 0
	while retry_attempt_counter < NUMBER_ATTEMPTS:
		try:
			content = request.text
			break
		except Exception as e:
			if retry_attempt_counter == NUMBER_ATTEMPTS:
				error_info = "Request timed out too many times. Skipping " + request.url 
				print(error_info)
				break
			else:
				print("Request timed out. Retrying...")
				retry_attempt_counter += 1

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
	Request shouldn't take more than a second or two
	'''
	try:
		request = requests.get(url_path, timeout = 1, stream = True)
	except Exception as e:

		error_info = "Error encountered pinging " + url_path + ". Defaulting to no ads.txt here."
		print(error_info)
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