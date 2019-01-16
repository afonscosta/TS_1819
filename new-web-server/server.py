import os
import re
import xattr
import string
import random
import smtplib, ssl
import subprocess
import pwd
from random import randrange
from flask import Flask, redirect, render_template, request, session, abort, send_file, url_for, make_response, send_from_directory
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    if request.form['username']:
        try :
            with open("/home/afonscosta/Documents/TS_1819/database.txt", "r") as fd:
                for line in fd:
                    info = re.split(r'::', line)
                    if request.form['username'] == info[0]:
                        print(info[0])
                        shutdown_server()
                        #return redirect('/')
        except (FileNotFoundError, KeyError):
            pass
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def do_register():
    if 'username' in request.form:
        try:
            with open("/home/afonscosta/Documents/TS_1819/database.txt", "a+") as fd:
                fd.write(request.form['username'] + '::' + request.form['email'] + '\n')
            return redirect('/')
        except KeyError:
            pass
    return render_template('register.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
