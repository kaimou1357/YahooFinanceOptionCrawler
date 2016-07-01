from flask import send_file, render_template, Flask, request, jsonify
import scraper
import json
import time
from collections import OrderedDict

app = Flask(__name__)


@app.route('/')
def root():
    return render_template("index.html")

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html'), 500

@app.route('/filegenerate', methods = ['GET'] )
def returncsvfile():
    file_name = request.args['inputTicker'] + "_options.csv"
    isList = True
    if request.args['viewoption'] == "straddleon":
    	isList = False
    try:

		scraper.processticker(request.args['inputTicker'], file_name, request.args['option_expiration'], isList)
		return send_file(file_name, as_attachment = True)
        
    except ValueError, IOError:
        return render_template("error.html")

	return render_template('index.html')

@app.route('/generate_dates', methods = ['GET'])
def generate_date():
    ticker = request.args['inputTicker']
    date_dictionary = scraper.generateExpirationDates(ticker)
    return jsonify(date_dictionary)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug = True)
