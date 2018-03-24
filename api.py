import functools
import os
import re
import pymongo
from bson.json_util import dumps

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response

# App Config
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', True)

# DB Config
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)
MONGODB_DB = os.environ.get('MONGODB_DB', 'podcast')

# App
app = Flask(__name__)

# DB
mongo_client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = mongo_client[MONGODB_DB]


@app.route('/users/tags', methods=['POST'])
def create_tags():
    ''' Add tag for the current user '''
    data = request.json
    if "tag" in data:
        db.user_tags.insert_one({"label": data["tag"]})
    return jsonify(data)


@app.route('/users/tags', methods=['GET'])
def get_users_tags():
    ''' Get all tags for the current user '''
    tags = [tag for tag in db.user_tags.find()]
    payload = dumps({'tags': tags})
    return Response(response=payload, mimetype="application/json")


@app.route('/users/tags', methods=['DELETE'])
def delete_users_tags():
    ''' Delete all tags for the current user '''
    db.user_tags.remove()
    return Response(status=201, mimetype="application/json")


@app.route('/tags')
def get_tags():
    ''' Get all tags '''
    tags = [tag for tag in db.tags.find()]
    payload = dumps({'tags': tags})
    return Response(response=payload, mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)
