import re
import time

from config import top_level_domains
from utils import *
from check_url import check_valid_url_ad_txt

class Extractor:


	def __init__(self, seller_website, app_package_name, ads_txt_regex = None):
		self.seller_website = seller_website
		self.app_package_name = app_package_name

		self.ads_txt_regex = None


	def look_for_ads_txt_url(self, entry_line):
		'''
		returns either a valid ads.txt location or an empty string ''
		'''

		def remove_subdomain(url):
			url_split_by_dots = url.split('.')
			for current_index, element in enumerate(url_split_by_dots):
				front = url_split_by_dots[:current_index]
				back = url_split_by_dots[current_index:]
				tld = '.'.join(back)
				if tld in top_level_domains:
					if len(front) > 1:
						front = front[1:]
						base_domain = '.'.join(front)
						
						if 'https' in url:
							http = "https://"
						else:
							http = "http://"
						return http + base_domain + '.' + tld
			return url

		def check_possible_url_validity(url):
			if 'http' in url.lower() and url != '':
				return True
			return False

		def check_description_in_metadata():
			'''
			Check the description property of the metadata for a URL 
			with an ads.txt scheme defined. e.g., 
			"adstxt://zynga.com/wordswithfriends/ads.txt". 
			If a valid ads.txt file exists, use it.
			This function is untested because we have no examples of this.
		
			'''
			if self.ads_txt_regex:
				ads_txt_regex = self.ads_txt_regex
			else:
				ads_txt_regex = r'(adstx.+?/ads.txt)'

			if 'ads.txt' in entry_line:
				find_ads_txt = re.search(ads_txt_regex, entry_line, re.IGNORECASE)
				if find_ads_txt:
					return find_ads_txt[0]

			return ''


		def check_entry_site_ads_txt_url(site_entry):
			'''
			Entire site entry + ads.txt. If the site entry is 
			"http://www.zynga.com/wordswithfriends" then look in 
			"http://www.zynga.com/wordswithfriends/ads.txt" for a 
			valid ads.txt file. If a valid ads.txt file exists, use it. 
			(skip further steps)

			'''
			possible_url = site_entry + 'ads.txt'
			possible_url = possible_url.replace('www.', '')

			if check_possible_url_validity(possible_url) and check_valid_url_ad_txt(possible_url):
				return possible_url
			return ''
			

		def check_full_domain_url(site_entry, package):
			'''
			If we don't find an ads.txt file there, then revert to 
			checking for the file at "http://{topleveldomain+1}/{appId}/ads.txt". 
			For the example above, we would look at 
			http://zynga.com/com.zynga.words3/ads.txt to see if there is 
			a valid ads.txt file.
			'''
			possible_url = site_entry + package + 'ads.txt'
			possible_url = possible_url.replace('www.', '')

			if check_possible_url_validity(possible_url) and check_valid_url_ad_txt(possible_url):
				return possible_url
			return ''
		
		'''
		all functions will either return a valid url or an empty string.
		We can use this format to then determine if we need to keep looking

		'''


		possible_url = ''

		site_entry_marker = self.seller_website
		site_entry = parse_for_specific_parameter(site_entry_marker, entry_line)
		site_entry = remove_subdomain(site_entry)
		site_entry = check_missing_slash(site_entry)
		package_marker = self.app_package_name
		package = parse_for_specific_parameter(package_marker, entry_line)
		package = check_missing_slash(package)

		#1
		possible_url = check_description_in_metadata()
		if possible_url != '':
			return possible_url

		#2
		possible_url = check_entry_site_ads_txt_url(site_entry)
		if possible_url != '':
			return possible_url
		#3
		possible_url = check_full_domain_url(site_entry, package)
		return possible_url


def open_file_create_dict(file_path, app_id_marker, market_url_marker, extractor):
	'''
	Opens up the data file and starts processing the data into a dictionary with format

	(app id, market url): ads.txt location

	'''
	ads_txt_location_dict = {}

	with open(file_path, 'r', encoding = 'utf-8') as f:
		current_entry = f.readline()
		while current_entry:
			app_id = parse_for_specific_parameter(app_id_marker, current_entry)
			market_url = parse_for_specific_parameter(market_url_marker, current_entry)
			if not app_id:
				print("Could not find title of app. Please investigate.")
			if not market_url:
				print("Could not find market url of app. Please investigate.")
			if app_id and market_url:
				if (app_id, market_url) not in ads_txt_location_dict:
					ads_txt_location_dict[(app_id, market_url)] = extractor.look_for_ads_txt_url(current_entry)
			current_entry = f.readline()
		f.close()
	return ads_txt_location_dict