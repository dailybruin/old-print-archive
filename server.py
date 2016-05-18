#DEBUG ONLY
from __future__ import print_function
import sys

from flask import Flask, render_template, send_from_directory, json, Response, jsonify, request
from flask.ext.pymongo import PyMongo
from flask.ext.cache import Cache
from datetime import datetime
from pymongo import MongoClient
from bson import json_util
import time
import os

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
        cached_results = cache.get("searchQueryResultCache-" + searchTerm)
        if cached_results is None:
            results = mongo.db.test_archive_collection.find(
                { '$text': { '$search': searchTerm } },
                { 'text': 0, '_id': 0, 'score' : { '$meta': 'textScore' }}
            )
            sorted_out = sorted(list(results), key=lambda r: r[u'score'], reverse=True)
            cache.set("searchQueryResultCache-" + searchTerm, sorted_out, 3600)
            data = sorted_out[page*10:page*10 + 10]
            len_items = results.count()
        else:
            data = cached_results[page*10:page*10 + 10]
            len_items = len(cached_results)
    elif not searchTerm:
        results = mongo.db.test_archive_collection.find(
            { 'date': {'$lt': endDate, '$gte': startDate} },
            { 'text': 0, '_id': 0, 'score' : { '$meta': 'textScore' }}
        ).sort([("date", -1),("page",1)])[page*10:page*10 + 10]
        data = list(results)
        len_items = results.count()
    else:
        results = mongo.db.test_archive_collection.find(
            { '$text': { '$search': searchTerm }, 'date': {'$lt': endDate, '$gte': startDate}},
            { 'text': 0, '_id': 0, 'score' : { '$meta': 'textScore' }}
        ).sort([("score", {'$meta': 'textScore'})])[page*10:page*10 + 10]
        data = list(results)
        len_items = results.count()
    res = {
        "query": searchTerm,
        "page": page + 1,
        "totalPages": int(len_items/10) + 1,
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

@app.route('/api/search')
def search():
    searchTerm = request.args.get('query', '')
    startDate = datetime.fromtimestamp(int(request.args.get('startDate', time.time()) ))
    endDate = datetime.fromtimestamp(int(request.args.get('endDate', time.time()) ))
    useDate = int(request.args.get('limitDate', 0))
    page = int(request.args.get('page', 1))-1

    return jsonify(searchDB(searchTerm, startDate, endDate, useDate, page))
    #return Response(json.dumps(data,default=json_util.default), mimetype='application/json')

if __name__ == '__main__':
    if os.environ.get('PRODUCTION') is None:
        app.debug = True
        app.run()
    else:
        app.run(host='0.0.0.0')
