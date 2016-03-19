from flask import send_file, render_template, Flask, request, jsonify
import scraper
import json

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
    try:
        #Temporarily added for Nathan to debug.
        scraper.processticker(request.args['inputTicker'], file_name, request.args['option_expiration'])
    except ValueError:
        return render_template("error.html")
    return send_file(file_name, as_attachment = True)

@app.route('/generate_dates', methods = ['GET'])
def generate_date():
    ticker = request.args['inputTicker']
    date_dictionary = scraper.generateExpirationDates(ticker)
    #print(json.dumps(date_dictionary))
    return jsonify(**date_dictionary)

if __name__ == "__main__":
    app.run(debug = True)
