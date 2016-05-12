from flask import flask
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/api/search/<searchterm>/')
def search():
