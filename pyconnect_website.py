from flask import Flask, render_template, request, session, g, redirect, url_for,abort, flash, json, jsonify
from pyconnect import *
from pyconnect_website_config import *
from flask_debugtoolbar import DebugToolbarExtension
import ctypes
import logging
import datetime
import time
import locale
import cgi


storage = cgi.FieldStorage()
locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__)
app.config.from_object(__name__)
a = Arduino(serial_port='COM8')
now = datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M:%S")
time.sleep(3)
LED_PIN = 10
ANALOG_PIN = 0
a.set_pin_mode(LED_PIN,'O')
print (now)
print ("Arduino инициализирована")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Неправильное имя пользователя'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Неправильный пароль'
        else:
            session['logged_in'] = True
            flash('Вы залогинились')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Вы разлогинились')
    return redirect(url_for('show_entries'))

@app.route('/', methods = ['POST','GET'])
def show_entries():
    author = "Brax"
    return render_template('show_entries.html', author=author)

@app.route('/datetime_content', methods = ['POST','GET'])
def datetime_content():
    nowdate_content = datetime.datetime.now().strftime("%a, %d.%m.%Yг.")
    nowtime_content = datetime.datetime.now().strftime("%H:%M")
    return render_template('datetime_content.html', nowdate_content=nowdate_content, \
    nowtime_content=nowtime_content)

@app.route('/analog_values', methods = ['POST','GET'])
def analog_values():
    readval = a.analog_read(ANALOG_PIN)
    return render_template('analog_values.html', valuet=round(100*(readval/1023.), 1))

@app.route('/press_button', methods = ['POST','GET'])
def press_button():
    if request.method == 'POST':
        if request.form['value'] == 'On':
            print ("ON")
            a.digital_write(LED_PIN,1)
        elif request.form['value'] == 'Off':
            print ("OFF")
            a.digital_write(LED_PIN,0)
        else:
            pass
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0')
