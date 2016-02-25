from bs4 import BeautifulSoup
import dryscrape
import json
import requests
import threading
import re
import csv
from multiprocessing import Pool


def main():

	base_url = 'http://finance.yahoo.com/q/op?s='
	ticker = raw_input(str("Enter the Ticker you would like to view Options Data for: "))

	base_url = base_url + ticker + "+Options"
	s = Scraper(base_url)
	#thr = threading.Thread(target = s.returnCallListAsJSON, args = (), kwargs = {})
	#p = Pool(5)
	#call_list = p.map(s.returnCallListAsJSON)
	call_list = s.returnCallListAsJSON()


def create_csv():
	create_copy = raw_input(str("Would you like to create a copy of the data (Yes/No)?"))

	if create_copy == 'Yes' or 'yes':
		csvfile = open("test.csv",'wb')
		csvwriter = csv.writer(csvfile, delimiter = ',')
		csvwriter.writerows(['Underlying Ticker', 'Strike Price', 'Ask', 'Bid'])
		for option in call_list:
			csvwriter.writerows([option['contractSymbol'], option['strike']['fmt'], option['ask']['fmt'], option['bid']['fmt']])
		csvfile.close()
	else:
		#make sure to use raw_input and not just input().
		raw_input("Would you like to search for another set of Option Data (Yes/No)?")

class Scraper(object):
	def __init__(self, base_url):
		self.r = requests.get(base_url)
		self.data = self.r.text
		self.soup = BeautifulSoup(self.data, 'lxml')
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
		#This needs to be implemented.
		scrape()


main()
