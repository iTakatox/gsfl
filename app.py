from flask import Flask, send_from_directory
import os

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)
