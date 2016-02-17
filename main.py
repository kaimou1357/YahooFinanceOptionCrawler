from bs4 import BeautifulSoup
import dryscrape
import json
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
		self.my_url = base_url
		self.session = dryscrape.Session()
		self.session.visit(self.my_url)
		self.response = self.session.body()
		self.soup = BeautifulSoup(self.response)
		
	def scrape(self):
		
		#Grab everything from google.finance.data to end of JSON.
		self.text = str(self.soup)
		self.startpoints = [(a.start(), a.end())for a in list(re.finditer("google.finance.data", self.text)) ]
		
		self.javascript_string = self.text[self.startpoints[0][0]:self.startpoints[1][0]]
		#grab the ending position of put JSON string
		self.put_ending_location = [a.end() for a in list(re.finditer("puts:", self.javascript_string))]
		self.call_starting_location = [a.end() for a in list(re.finditer("calls:", self.javascript_string))]
		#print(self.put_ending_location)
		#print(self.call_starting_location)

		self.put_json_string = json.dumps(self.javascript_string[self.put_ending_location[0]: self.call_starting_location[0]-7])
		#Removed the backslashes
		self.put_json_string = self.put_json_string.replace("\\", "")
		print(self.put_json_string)
		#self.put_json_list = json.loads('{cid:"564463958661698",name:"",s:"AAPL160219P00081000",e:"OPRA",p:"0.01",cs:"chr",c:"-0.04",cp:"-80.00",b:"0.01",a:"0.02",oi:"10515",vol:"1543",strike:"81.00",expiry:"Feb 19, 2016"}')


		
	
	def returnCallListAsJSON(self):
		scrape()

	def returnPutListAsJSON(self):
		scrape()

#Implement a way to POST parameters via user input rather than hard code.
s = Scraper('https://www.google.com/finance/option_chain?q=NASDAQ%3AIBM')
s.scrape()



