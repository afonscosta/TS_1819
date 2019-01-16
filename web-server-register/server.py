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
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def do_register():
    if 'email' in request.form:
        print(request.form['email'])
        shutdown_server()
        return redirect('/')
    return render_template('register.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
