from bs4 import BeautifulSoup
import dryscrape
import json
import requests
import re

class Option(object):
	def __init__(self):
		self.strike = 0.0
		self.price = 0.0
		self.change = 0.0
		self.bid = 0.0
		self.ask = 0.0
		self.volume = 0.0
		self.open_int = 0.0


class Scraper(object):
	def __init__(self, base_url):
		self.r = requests.get(base_url)
		self.data = self.r.text
		self.soup = BeautifulSoup(self.data)
		self.list = []
		for n in self.soup.find_all('script'):
			self.list.append(n)

		#16th index is the correct string we want for AAPL at least.

	def scrape(self):
		#cast object to a string to parse for "calls" tag
		raw_options_chain = str(self.list.pop(16))

		startoptions = [a.start() for a in list(re.finditer('calls', raw_options_chain))]
		endoptions = [a.start() for a in list(re.finditer('_options', raw_options_chain))]
		
		raw_options_chain = raw_options_chain[startoptions[0]-2:endoptions[0]-2]

		options_json = json.loads(raw_options_chain)
		print(options_json)
	
		
	
	def returnCallListAsJSON(self):
		scrape()

	def returnPutListAsJSON(self):
		scrape()

#Implement a way to POST parameters via user input rather than hard code.
s = Scraper('http://finance.yahoo.com/q/op?s=AAPL+Options')
s.scrape()



