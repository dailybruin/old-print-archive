from flask import Flask, render_template, send_from_directory, json, Response, jsonify
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from bson import json_util
import os

class NotConfiguredException(Exception):
    pass

app = Flask(__name__)

#Database Config
mongo_uri = os.environ.get('MONGO_URI')
if mongo_uri is None:
    raise NotConfiguredException("Database URL not configured!")

app.config['MONGO_URI'] = mongo_uri
mongo = PyMongo(app)

#Serve Static
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/api/search/<searchterm>')
@app.route('/api/search/<searchterm>/<page>')
def search(searchterm, page=1):
    results = mongo.db.test_archive_collection.find(
        { '$text': { '$search': searchterm } },
        { 'text': 0, '_id': 0, 'score' : { '$meta': 'textScore' }}
    )
    page = int(page) - 1
    data = sorted(list(results), key=lambda r: r[u'score'], reverse=True)[page*10:page*10 + 10]
    res = {
        "page": page + 1,
        "totalPages": int(results.count()/10) + 1,
        "totalItems": results.count(),
        "data": data
    }
    return jsonify(res)
    #return Response(json.dumps(data,default=json_util.default), mimetype='application/json')

if __name__ == '__main__':
    if os.environ.get('PRODUCTION') is None:
        app.debug = True
        app.run()
    else:
        app.run(host='0.0.0.0')
