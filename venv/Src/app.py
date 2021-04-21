from flask import Flask, render_template, url_for
from mongo import Mongo_Client

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])

def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
