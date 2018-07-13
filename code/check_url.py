import requests


def check_valid_url_ad_txt(url_path):
	'''
	Given a url, we try to check if it is valid. Returns a boolean 
	'''
	request = requests.get(url_path)
	if request.status_code == 200:
		return True
	return False

