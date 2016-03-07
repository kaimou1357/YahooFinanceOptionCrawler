from flask import send_file, render_template, Flask, request
from bs4 import BeautifulSoup
import dryscrape
import json
import requests
import re
import csv
import sys
app = Flask(__name__)

server_directoy = "/home/psp219/YahooFinanceOptionCrawler/"

def create_csv(call_list, file_name):

    csvfile = open(file_name,'wb')
    csvwriter = csv.writer(csvfile, delimiter = ',')
    csvwriter.writerow(['Underlying Ticker', 'Strike Price', 'Ask', 'Bid','Volume','Open Interest'])
    for option in call_list:
        if option['volume']['fmt'] != "0" and option['ask']['fmt'] != '0' and option['bid']['raw'] != 0 and option['openInterest']['fmt'] != '0':
            csvwriter.writerow([option['contractSymbol'], option['strike']['fmt'], option['ask']['fmt'], option['bid']['fmt'], option['volume']['fmt'], option['openInterest']['fmt']])
    csvfile.close()


def processticker(ticker, file_name):
    base_url = "http://finance.yahoo.com/q/op?s=" + ticker + "+Options"
    num_of_tries = 0
    while num_of_tries<20:
        try:
            r = requests.get(base_url)
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            option_list = []
            for n in soup.find_all('script'):
                option_list.append(n)
            raw_options_chain = str(option_list.pop(16))
            startoptions = [a.start() for a in list(re.finditer('calls', raw_options_chain))]
            endoptions = [a.start() for a in list(re.finditer('_options', raw_options_chain))]
            raw_options_chain = raw_options_chain[startoptions[0]-2:endoptions[0]-2]
            options_json = json.loads(raw_options_chain)
            calls_list = options_json['calls']
            create_csv(calls_list, file_name)

        except IndexError:
            num_of_tries+=1
            continue
        break


@app.route('/')
def root():
    return render_template("index.html")

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html'), 500

@app.route('/filegenerate', methods = ['GET'] )
def returncsvfile():
    file_name = request.args['inputTicker'] + "_options_info.csv"
    try:
        processticker(request.args['inputTicker'], file_name)
    except ValueError:
        return render_template("index.html")
    return send_file(file_name, as_attachment = True)

if __name__ == "__main__":
    app.run()
