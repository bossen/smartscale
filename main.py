#!/bin/python2
import os, gzip, StringIO, time, csv, datetime
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)
CSV_FILENAME = "smartscale.csv"

types = ["weight", "body fat", "body water", "muscle", "bone mass", "calories"]

@app.route('/stats')
def stats():
    with open(CSV_FILENAME) as f:
        csv = f.read().splitlines() 
    data = [(line.split(',')) for line in csv]

    return render_template('chart.html', types=types, values=data)

    #return str(data)

@app.route('/', methods=['POST'])
def upload_file():
    data = request.get_data()
    values = [d.split('=')[1] for d in data.split('&')]

    if values and "%" not in data:
        filename = CSV_FILENAME
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(filename, "a") as fh:
            fh.write(','.join(values) + "," + timestr + "\n")

        #return 'sucess'
    return 'error'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
