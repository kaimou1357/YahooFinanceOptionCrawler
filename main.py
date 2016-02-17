from bs4 import BeautifulSoup
import dryscrape
import json
import re


class Scraper(object):
	def __init__(self, base_url):
		self.my_url = base_url
		self.session = dryscrape.Session()
		self.session.visit(self.my_url)
		self.response = self.session.body()
		self.soup = BeautifulSoup(self.response)
		
	def scrape(self):
		return str(self.soup)


#Implement a way to POST parameters via user input rather than hard code.
s = Scraper('https://www.google.com/finance/option_chain?q=NASDAQ%3AIBM')
text = s.scrape()
#text contains HTML and JS
startpoints = [(a.start(), a.end())for a in list(re.finditer("google.finance.data", text)) ]
javascript_string = text[startpoints[0][0]:startpoints[1][0]]
print(javascript_string)

