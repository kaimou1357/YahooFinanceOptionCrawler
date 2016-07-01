import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import json
import csv

server_directory = "/home/psp219/YahooFinanceOptionCrawler/"
yahoo_url = "http://finance.yahoo.com"

def create_csv(call_list, put_list, file_name, listview):
    
    csvfile = open(file_name,'wb')
    csvwriter = csv.writer(csvfile, delimiter = ',')
    if not listview:

        csvwriter.writerow(['Call Information', '', '', '', '', '',"",'Put Information' ])
        csvwriter.writerow(['Underlying Ticker', 'Bid', 'Ask','Volume','Open Interest', 'Expiration Date', 'Strike Price', 'Underlying Ticker', 'Bid', 'Ask','Volume','Open Interest', 'Expiration Date'])
        callPrinted = False
        putPrinted = False
        for i in range(len(call_list)):
            #print(call_list[i])
            if call_list[i]['volume']['raw'] != 0 and call_list[i]['ask']['raw'] != 0 and call_list[i]['bid']['raw'] != 0 and call_list[i]['openInterest']['raw'] != 0:
                callPrinted = True
                #csvwriter.writerow([option['contractSymbol'], option['bid']['fmt'], option['ask']['fmt'], option['volume']['fmt'], option['openInterest']['fmt'], option['expiration']['fmt'], option['strike']['fmt']])
            if put_list[i]['volume']['raw'] != 0 and put_list[i]['ask']['raw'] != 0 and put_list[i]['bid']['raw'] != 0 and put_list[i]['openInterest']['raw'] != 0:
                putPrinted = True
            if (not callPrinted)and (not putPrinted):
                csvwriter.writerow(["", "", "", "", "", "", call_list[i]['strike']['fmt']])

            if putPrinted and callPrinted:
                csvwriter.writerow([call_list[i]['contractSymbol'], call_list[i]['bid']['fmt'], call_list[i]['ask']['fmt'], call_list[i]['volume']['fmt'], call_list[i]['openInterest']['fmt'], call_list[i]['expiration']['fmt'], call_list[i]['strike']['fmt'], put_list[i]['contractSymbol'], put_list[i]['bid']['fmt'], put_list[i]['ask']['fmt'], put_list[i]['volume']['fmt'], put_list[i]['openInterest']['fmt'], put_list[i]['expiration']['fmt']])
                putPrinted = False
                callPrinted = False

                #print both call and puts
                #assign callPrinted and putPrinted to false
            if putPrinted and (not callPrinted):
                csvwriter.writerow(['', '', '', '', '', '', call_list[i]['strike']['fmt'], put_list[i]['contractSymbol'], put_list[i]['bid']['fmt'], put_list[i]['ask']['fmt'], put_list[i]['volume']['fmt'], put_list[i]['openInterest']['fmt'], put_list[i]['expiration']['fmt']])
                putPrinted = False

                #print puts and assign putPrinted to false
            if callPrinted and (not putPrinted):
                csvwriter.writerow([call_list[i]['contractSymbol'], call_list[i]['bid']['fmt'], call_list[i]['ask']['fmt'], call_list[i]['volume']['fmt'], call_list[i]['openInterest']['fmt'], call_list[i]['expiration']['fmt'], call_list[i]['strike']['fmt']])
                callPrinted = False

    else:
        csvwriter.writerow(['Call Information'])
        csvwriter.writerow(['Underlying Ticker', 'Bid', 'Ask','Volume','Open Interest', 'Expiration Date'])
        for option in call_list:
            if option['volume']['fmt'] != "0" and option['ask']['fmt'] != '0' and option['bid']['raw'] != 0 and option['openInterest']['fmt'] != '0':
                csvwriter.writerow([option['contractSymbol'], option['bid']['fmt'], option['ask']['fmt'], option['volume']['fmt'], option['openInterest']['fmt'], option['expiration']['fmt'], option['strike']['fmt']])
        else:
            csvwriter.writerow(["", "", "", "", "", "", option['strike']['fmt']])
        csvwriter.writerow(['Put Information'])
        for option in put_list:
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
    #print(od)

    return expiration_dictionary

def processticker(ticker, file_name, date_int, listview):
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
            print(call_list)
            create_csv(call_list, put_list, file_name, listview)

        except IndexError:
            num_of_tries+=1
            continue
        break
