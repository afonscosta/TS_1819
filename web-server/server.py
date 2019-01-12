import os
import re
from flask import Flask, flash, redirect, render_template, request, session, abort, send_file, url_for

app = Flask(__name__)

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
    # return home()

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

@app.route('/filesystem')
def fs():
    if not session.get('logged_in'):
        return render_template('login.html')
    return dir_listing('')#render_template('filemanager.html')

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    base_dir = os.environ['HOME']

    # Joining the base and the requested path
    abs_path = os.path.join(base_dir, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    print('entrou')
    full_path = []
    # Show directory contents
    files = os.listdir(abs_path)
    for f in files:
        path = re.split(r'(?<![\\])/', req_path)[-1:]
        full_path.append((path[0] + '/', f))

    return render_template('files.html', files=full_path)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
