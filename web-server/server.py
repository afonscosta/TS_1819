import os
import re
import xattr
import string
import random
import smtplib, ssl
import subprocess
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
    if not session.get('logged_in'):
        return render_template('login.html')
    if request.method == 'POST':
        if 'logout' in request.form:
            return logout()
        if 'start' in request.form:
            return dir_listing('')
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'p' and request.form['username'] == 'a':
        session['logged_in'] = True
        return redirect('/')
    else:
        flash('wrong password!')
    return render_template('login.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')

def send_email(pw):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "ts.1819.teste@gmail.com"
    to_addrs = "" #<-------------------------------------------------------------------- INSERIR EMAIL DO RECETOR
    password = "tecseg1819"
    message = 'To: {}\r\nSubject: {}\r\n\r\n{}'.format(to_addrs, 'Password do ficheiro', pw)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, [to_addrs], message)


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
@nocache
def dir_listing(req_path):
    base_dir = os.environ['HOME']

    # Joining the base and the requested path
    abs_path = os.path.join(base_dir, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        try:
            n = randrange(10, 21)
            newpass = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(n))
            print(newpass)
            send_email(newpass)
            xattr.set(abs_path, 'user.pass', newpass + '\0')
            print(xattr.get(abs_path, 'user.pass'))
            prefix_path = re.split(r'(?<![/:])/', request.referrer)[:1][0]
            req_path = "/".join(re.split(r'(?<![\\])/', req_path)[:-1])
            return render_template('pass.html', path=prefix_path + '/' + req_path)#pass_check(abs_path)
        except PermissionError:
            req_path = "/".join(re.split(r'(?<![\\])/', req_path)[:-1])
            abs_path = os.path.join(base_dir, req_path + '/')
            return redirect(req_path)

    full_path = []
    # Show directory contents
    files = os.listdir(abs_path)
    for f in files:
        path = re.split(r'(?<![\\])/', req_path)[-1:]
        full_path.append((path[0] + '/', f))

    return render_template('files.html', files=full_path)

@app.route('/pass', methods=['GET', 'POST'])
def pass_check():
    base_dir = os.environ['HOME']
    prefix_path = re.split(r'(?<![\\])/', request.referrer)[:1][0]
    req_path = '/'.join(re.split(r'/', request.referrer)[3:])
    abs_path = base_dir + '/' + req_path

    try:
        if request.method == 'POST':
            if not request.form['password']:
                aux = re.split(r'/', req_path)[:-1]
                req_path = '/'.join(aux)
                return render_template('pass.html', path=prefix_path + req_path)
            xattr.set(abs_path, 'user.try', request.form['password'] + '\0')
            print(xattr.get(abs_path, 'user.try'))
            return send_file(abs_path)
    except PermissionError:
        aux = re.split(r'/', req_path)[:-1]
        req_path = '/'.join(aux)
        return redirect(req_path)

    aux = re.split(r'/', req_path)[:-1]
    req_path = '/'.join(aux)
    return render_template('pass.html', path=prefix_path + req_path)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
