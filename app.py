import datetime
import sqlite3
import re
import base64
import os

from flask import Flask, render_template, request, redirect,  flash, url_for
app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'for dev')
reg = re.compile(r'\d{11}|\d{9}')

def obscure_id(raw_id):
    """ Obscure ID number """
    idsearch = reg.search(raw_id)
    try:
        id_number = idsearch.group()[-9:].encode('utf-8')
    except AttributeError:
        return None
    e_id = base64.b64encode(id_number)
    return e_id

@app.route('/')
def front_page():
    try:
        building_str = ' '.join(request.args.get('building').split('_'))
    except AttributeError:
        building_str = ''
    building = request.args.get('building')
    return render_template('barcode.html', building=building, building_str=building_str)

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        building = request.args.get('building')
        print(building)
        # Get variable from form data
        form_data = request.form
        raw_id = form_data['id_number']
        e_id = obscure_id(raw_id)
        ip = request.headers['X-Real-IP']
        if not e_id:
            flash("Barcode scan failed. Please try again.","alert-danger")
            return redirect('\\')
        with sqlite3.connect("covid_scan.sqlite") as con:
            c = con.cursor()
            c.execute(f"INSERT INTO entries (id_number, day, time, ip_address) VALUES (?, ?, ?, ?)", (e_id, datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%X'), ip))
        flash("260***{}. You have successfully signed in at {} ".format(raw_id[-3:], datetime.datetime.now().strftime('%X')), "alert-success")
        return redirect(url_for('front_page', building=building))

if __name__ == '__main__':
    app.debug = True
    app.run()
