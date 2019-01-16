import os
from flask import Flask, render_template, request, abort, url_for

app = Flask(__name__)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['password']:
            print(request.form['password'])
            shutdown_server()
            return render_template('done.html')
    return render_template('index.html')


@app.route('/timeout', methods=['GET'])
def timeout():
    shutdown_server()
    return render_template('timeout.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
