import re
import time
import json
import functools

from top_level_domains import top_level_domains
from utils import check_missing_slash
from check_url import check_valid_url_ad_txt

class Extractor:
	"""
	This class helps find the possible ads.txt url locations for a given data entry. 
	It does this by parsing the data for possible urls and also constructing them using
	a format. It then pings these urls and checks their validity.
	"""

	def __init__(self, seller_website, app_package_name):
		self.seller_website = seller_website
		self.app_package_name = app_package_name
		self.ads_txt_regex = None




	def _check_possible_url_validity(self, url):
		return url and re.match('http', url, re.IGNORECASE)

	def _remove_subdomain(self, url):
		"""
		helps remove subdomains from an url, 
		logic translated from current C# logic in prod
		"""
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
						http = 'https://'
					else:
						http = 'http://'
					return http + base_domain + '.' + tld
		return url


	def _check_description_in_metadata(self, entry_line):
		"""
		Check the description property of the metadata for a URL 
		with an ads.txt scheme defined. e.g., 
		"adstxt://zynga.com/wordswithfriends/ads.txt". 
		If a valid ads.txt file exists, use it.
		This function is untested because we have no examples of this.
		"""

		if self.ads_txt_regex:
			ads_txt_regex = self.ads_txt_regex
		else:
			ads_txt_regex = r'adstx.+?/ads\.txt'

		if 'ads.txt' in entry_line:
			find_ads_txt = re.search(ads_txt_regex, entry_line, re.IGNORECASE)
			if find_ads_txt:
				return find_ads_txt[0]

		return ''

	def _check_url_all(self, possible_url):
		if self._check_possible_url_validity(possible_url) and check_valid_url_ad_txt(possible_url):
			return possible_url
		return ''


	@functools.lru_cache(maxsize=1024)
	def _check_full_domain_url(self, site_entry, package):
		"""
		If we don't find an ads.txt file there, then revert to 
		checking for the file at "http://{topleveldomain+1}/{appId}/ads.txt". 
		For the example above, we would look at 
		http://zynga.com/com.zynga.words3/ads.txt to see if there is 
		a valid ads.txt file.
		"""

		possible_url = site_entry + package + 'ads.txt'
		possible_url = possible_url.replace('www.', '')
		return self._check_url_all(possible_url)
	


	def look_for_ads_txt_url(self, entry_line):
		"""
		returns either a valid ads.txt location or an empty string ''
		"""

		
		"""
		all functions will either return a valid url or an empty string.
		We can use this format to then determine if we need to keep looking

		"""

		possible_url = ''

		site_entry_marker = self.seller_website
		site_entry = entry_line.get(site_entry_marker, '')
		if not site_entry: #if we can't find original app creator, give up and go to next entry
			return possible_url
		site_entry = self._remove_subdomain(site_entry)
		site_entry = check_missing_slash(site_entry)
		package_marker = self.app_package_name
		package = entry_line.get(package_marker, '')
		if package: #protect against error when it is None
			package = check_missing_slash(package)
		else:
			package = ''

		#1
		possible_url = self._check_description_in_metadata(entry_line)
		if possible_url != '':
			return possible_url

		#2
		possible_url = self._check_full_domain_url(site_entry, package)
		return possible_url
