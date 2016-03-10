from flask import send_file, render_template, Flask, request
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
        scraper.generateExpirationDates(request.args['inputTicker'])
    except ValueError:
        return render_template("error.html")
    return send_file(file_name, as_attachment = True)

if __name__ == "__main__":
    app.run(debug = True)
