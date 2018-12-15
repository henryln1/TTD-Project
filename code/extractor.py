import re
import time
import json
import functools
from urllib.parse import urlparse

from top_level_domains import top_level_domains
from utils import check_missing_slash
from check_url import check_valid_url_ad_txt

class Extractor:
	"""
	This class helps find the possible ads.txt url locations for a given data entry. 
	It does this by parsing the data for possible urls and also constructing them using
	a format. It then pings these urls and checks their validity.
	"""

	def __init__(self, seller_website):
		self.seller_website = seller_website
		self.ads_txt_regex = None




	def _check_possible_url_validity(self, url):
		return url and re.match('http', url, re.IGNORECASE)

	def _normalize_url(self, url, subdomains_to_leave=1):
		"""
		helps remove subdomains from an url, 
		logic translated from current C# logic in prod
		"""
		parsed_url = urlparse(url)
		domain = parsed_url.netloc
		url_split_by_dots = domain.split('.')
		for current_index, element in enumerate(url_split_by_dots):
			front = url_split_by_dots[:current_index]
			back = url_split_by_dots[current_index:]
			tld = '.'.join(back)
			if tld in top_level_domains:
				if len(front) > subdomains_to_leave:
					front = front[len(front) - subdomains_to_leave:]
				base_domain = '.'.join(front)
				return parsed_url.scheme +'://' + base_domain + '.' + tld
		return url

	def _check_url_all(self, possible_url):
		if self._check_possible_url_validity(possible_url) and check_valid_url_ad_txt(possible_url):
			return possible_url
		return ''


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

		site_entry = check_missing_slash(self._normalize_url(site_entry, 2))
		possible_url = self._check_url_all(site_entry + 'app-ads.txt')
		if possible_url == '':
			site_entry = check_missing_slash(self._normalize_url(site_entry, 1))
			possible_url = self._check_url_all(site_entry + 'app-ads.txt')
		return possible_url
