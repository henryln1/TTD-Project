import requests
import re


def extensive_check_for_ads_txt(request):
	'''
	After performing the initial status code check, we now need to check for soft 404s and other annoying things
	to verify whether or not there is a ads.txt file present. Boolean function

	'''
	content = request.text

	if ((
		'<!DOCTYPE' in content or 
		'<!doctype' in content or 
		'<html' in content or 
		'<HTML' in content or 
		'<content:encoded' in content) 
	and
		('DIRECT' in content or 
		'RESELLER' in content or 
		'direct' in content or 
		'reseller' in content)
	and (not re.search('Page not found', content, re.IGNORECASE))):
		return True


	return False



def check_valid_url_ad_txt(url_path):
	'''
	Given a url, we try to check if it is valid. Returns a boolean 
	'''
	request = requests.get(url_path)
	if request.status_code == 200:
		return extensive_check_for_ads_txt(request)
	return False

