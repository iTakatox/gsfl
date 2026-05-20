from flask import Flask, render_template, session, redirect, url_for, request
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'gs-injury-tool-2026-secret')

PASSWORD = os.environ.get('APP_PASSWORD', '19791118')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.before_request
def check_auth():
    if request.endpoint not in ('login', 'static') and not session.get('authenticated'):
        if request.endpoint != 'login':
            return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        error = '密码错误，请重试'
    return render_template('login.html', error=error)


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)
