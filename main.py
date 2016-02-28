from bs4 import BeautifulSoup
import dryscrape
import json
import requests
import threading
import re

def main():

	base_url = 'http://finance.yahoo.com/q/op?s='
	ticker = raw_input(str("Enter the Ticker you would like to view Options Data for: "))

	base_url = base_url + ticker + "+Options"



	s = Scraper(base_url)
	call_list = s.returnCallListAsJSON()

	for option in call_list:
		print(option['contractSymbol'])

class Scraper(object):
	def __init__(self, base_url):
		self.r = requests.get(base_url)
		self.data = self.r.text
		self.soup = BeautifulSoup(self.data)
		self.list = []
		for n in self.soup.find_all('script'):
			self.list.append(n)


	def returnCallListAsJSON(self):
		#16th index will give us the correct <script> tags for options_chain data.
		raw_options_chain = str(self.list.pop(16))

		startoptions = [a.start() for a in list(re.finditer('calls', raw_options_chain))]
		endoptions = [a.start() for a in list(re.finditer('_options', raw_options_chain))]

		raw_options_chain = raw_options_chain[startoptions[0]-2:endoptions[0]-2]

		options_json = json.loads(raw_options_chain)

		calls_list = options_json['calls']

		return calls_list
	def returnPutListAsJSON(self):
		scrape()


main()
#Implement a way to POST parameters via user input rather than hard code.
