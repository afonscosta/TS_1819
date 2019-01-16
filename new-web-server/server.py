import os
import re
import xattr
import string
import random
import smtplib, ssl
import subprocess
import pwd
from random import randrange
from flask import Flask, flash, redirect, render_template, request, session, abort, send_file, url_for, make_response, send_from_directory
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    if request.form['username']:
        try :
            with open("database.txt", "r+") as fd:
                for line in fd:
                    info = re.split(r'::', line)                    
                    if request.form['username'] == info[0]: 
                        print(line.rstrip())
                        os._exit(0)
                        #return redirect('/')
                flash('username not found!')
        except (FileNotFoundError, KeyError):
            flash('username not found!')
    else:
        flash('wrong password!')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def do_register():
    if 'username' in request.form:
        try:
            with open("database.txt", "a+") as fd:
                fd.write(request.form['username'] + '::' + request.form['email'] + '\n')
            return redirect('/')
        except KeyError:
            flash('username not found!')
    else:
        flash('wrong password!')
    return render_template('register.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)

