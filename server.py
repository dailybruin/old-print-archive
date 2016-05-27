from flask import Flask, render_template, send_from_directory, json, Response, jsonify, request
from flask.ext.pymongo import PyMongo
from flask.ext.cache import Cache
from datetime import datetime
from pymongo import MongoClient
from bson import json_util
import time
import os
import re

class NotConfiguredException(Exception):
    pass

app = Flask(__name__)

#Database Config
mongo_uri = os.environ.get('MONGO_URI')
redis_uri = os.environ.get('REDIS_URI')
if mongo_uri is None or redis_uri is None:
    raise NotConfiguredException("Database URL not configured!")

app.config['MONGO_URI'] = mongo_uri
app.config['CACHE_REDIS_URL'] = redis_uri
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600
mongo = PyMongo(app)
cache = Cache(app)

@cache.memoize(timeout=3600)
def searchDB(searchTerm, startDate, endDate, useDate, page):
    if useDate is 0:
        results = mongo.db.test_archive_collection.find(
            { '$text': { '$search': searchTerm } },
            { '_id': 0, 'score' : { '$meta': 'textScore' }}
        ).sort([("score", {'$meta': 'textScore'})]).limit(2000)[page*10:page*10 + 10]
    elif not searchTerm:
        results = mongo.db.test_archive_collection.find(
            { 'date': {'$lt': endDate, '$gte': startDate} },
            { '_id': 0, 'score' : { '$meta': 'textScore' }}
        ).sort([("date", 1),("page",1)]).limit(2000)[page*10:page*10 + 10]
    else:
        results = mongo.db.test_archive_collection.find(
            { '$text': { '$search': searchTerm }, 'date': {'$lt': endDate, '$gte': startDate}},
            { '_id': 0, 'score' : { '$meta': 'textScore' }}
        ).sort([("score", {'$meta': 'textScore'})]).limit(2000)[page*10:page*10 + 10]
    data = list(results)
    for r in data:
        try:
            r['text'] = re.search('[^\s]+.{,100}' + searchTerm + '.{,100}[^\s]*', r['text'], re.IGNORECASE | re.DOTALL).group(0)
        except:
            r['text'] = "Unable to find match"
    len_items = results.count()
    if len_items > 2000:
        max_items = 2000
    else:
        max_items = len_items
    res = {
        "query": searchTerm,
        "page": page + 1,
        "totalPages": int(max_items/10) + 1,
        "totalItems": len_items,
        "data": data
    }
    return res

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

@app.route('/search')
def searchPage():
    return render_template("search.html")

@app.route('/api/search')
def search():
    searchTerm = request.args.get('query', '')
    useDate = int(request.args.get('limitDate', 0))
    page = int(request.args.get('page', 1))-1
    startDate = datetime.fromtimestamp(int(request.args.get('startDate', time.time()) ))   
    endDate = datetime.fromtimestamp(int(request.args.get('endDate', time.time()) ))

    return jsonify(searchDB(searchTerm, startDate, endDate, useDate, page))
    #return Response(json.dumps(data,default=json_util.default), mimetype='application/json')

if os.environ.get('PRODUCTION') is None:
    @app.route('/test')
    def test():
        return render_template("test.html")

    @app.route('/test/clearcache')
    def clearcache():
        try:
            cache.clear()
        except:
            return "Failed"
        return "Done!"

if __name__ == '__main__':
    if os.environ.get('PRODUCTION') is None:
        app.debug = True
        app.run()
    else:
        app.run(host='0.0.0.0')
