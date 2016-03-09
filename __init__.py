from flask import send_file, render_template, Flask, request
from bs4 import BeautifulSoup
import json
import requests
import re
import csv
app = Flask(__name__)

server_directory = "/home/psp219/YahooFinanceOptionCrawler/"

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
    app.run(debug = True)
