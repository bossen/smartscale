#!/bin/python2
import os, gzip, StringIO, time, csv, datetime
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from wtforms import Form, DecimalField, validators

class UpdateForm(Form):
    weight = DecimalField('Weight', [validators.DataRequired()])
    fat = DecimalField('Body fat', [validators.DataRequired()])
    water = DecimalField('Body water', [validators.DataRequired()])
    muscle = DecimalField('Muscle', [validators.DataRequired()])
    bonemass = DecimalField('Bone mass', [validators.DataRequired()])
    calories = DecimalField('Calories', [validators.DataRequired()])


app = Flask(__name__)
CSV_FILENAME = "smartscale.csv"

types = ["weight", "fat", "water", "muscle", "bonemass", "calories"]

@app.route('/stats')
def stats():
    with open(CSV_FILENAME) as f:
        csv = f.read().splitlines() 
    data = [(line.split(',')) for line in csv]
    return render_template('chart.html', types=types, values=data)

def updateData(data):
    values = []
    for t in types:
        values.append(str(data[t]))

    filename = CSV_FILENAME
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open(filename, "a") as fh:
        fh.write(','.join(values) + "," + timestr + "\n")

@app.route('/', methods=['GET', 'POST'])
def update():
    form = UpdateForm(request.form)
    if request.method == 'POST' and form.validate():
        updateData(form.data)
        return redirect('stats')

    return render_template('update.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
