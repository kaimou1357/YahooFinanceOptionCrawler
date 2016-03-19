import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import json
import csv

server_directory = "/home/psp219/YahooFinanceOptionCrawler/"
yahoo_url = "http://finance.yahoo.com"

def create_csv(call_list, put_list, file_name):

    csvfile = open(file_name,'wb')
    csvwriter = csv.writer(csvfile, delimiter = ',')
    csvwriter.writerow(['Call Information'])
    csvwriter.writerow(['Underlying Ticker', 'Bid', 'Ask','Volume','Open Interest', 'Expiration Date'])
    for option in call_list:
        if option['volume']['fmt'] != "0" and option['ask']['fmt'] != '0' and option['bid']['raw'] != 0 and option['openInterest']['fmt'] != '0':
            csvwriter.writerow([option['contractSymbol'], option['bid']['fmt'], option['ask']['fmt'], option['volume']['fmt'], option['openInterest']['fmt'], option['expiration']['fmt'], option['strike']['fmt']])
        else:
            csvwriter.writerow(["", "", "", "", "", "", option['strike']['fmt']])
    csvfile.close()

def generateExpirationDates(ticker):
    base_url = "http://finance.yahoo.com/q/op?s=" + ticker + "+Options"
    r = requests.get(base_url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    option_list = []
    expiration_dictionary  = {}
    for pair in soup.find_all('option'):
        #get last 10 digits of the int. This will give us the correct integer for the date that the user clicked.
        expiration_dictionary[int(pair['value'])] = pair.get_text()
    #Debug Code
    od = OrderedDict(sorted(expiration_dictionary.items(), key = lambda t: t[1]))
    #print(od)

    return od

def processticker(ticker, file_name, date_int):
    base_url = "http://finance.yahoo.com/q/op"
    num_of_tries = 0
    payload = {'s' : ticker, 'date': date_int}
    r = requests.get(base_url, params = payload)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    option_list = []
    expiration_dictionary  = {}

    while num_of_tries<20:
        try:

            for pair in soup.find_all('option'):
                expiration_dictionary[pair.get_text()] = yahoo_url + pair['data-selectbox-link']
            for n in soup.find_all('script'):
                option_list.append(n)
            raw_options_chain = str(option_list.pop(16))
            start_call_options = [a.start() for a in list(re.finditer('calls', raw_options_chain))]
            endoptions = [a.start() for a in list(re.finditer('_options', raw_options_chain))]
            raw_options_chain = raw_options_chain[start_call_options[0]-2:endoptions[0]-2]
            options_json = json.loads(raw_options_chain)
            #Extract puts/calls as JSON objects.
            put_list = options_json['puts']
            call_list = options_json['calls']
            create_csv(call_list, put_list, file_name)

        except IndexError:
            num_of_tries+=1
            continue
        break
