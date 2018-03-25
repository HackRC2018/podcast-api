import functools
import os
import re
import random
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
    """ Add tag for the current user """
    data = request.json
    if "tag" in data:
        db.user_tags.insert_one({"label": data["tag"]})
    return jsonify(data)


@app.route('/users/tags', methods=['GET'])
def get_users_tags():
    """ Get all tags for the current user """
    tags = db.user_tags.find()
    payload = dumps({'tags': tags})
    return Response(response=payload, mimetype="application/json")


@app.route('/users/tags', methods=['DELETE'])
def delete_users_tags():
    """ Delete all tags for the current user """
    db.user_tags.remove()
    payload = dumps({})
    return Response(response=payload, status=204, mimetype="application/json")


@app.route('/tags')
def get_tags():
    """ Get all tags """
    tags = list(db.tags.find())
    users_tags = list(db.user_tags.find())

    # Get tags not used by the user
    id_tags = [tag['label'] for tag in tags]
    id_users_tags = [tag['label'] for tag in users_tags]
    id_diff = list(set(id_tags) - set(id_users_tags))
    tags_to_return = []
    for tag in tags:
        if tag['label'] in id_diff:
            tags_to_return.append(tag)

    # Randomly select tags to return
    if len(tags_to_return) >= 12:
        tags_to_return = random.sample(tags_to_return, 12)

    payload = dumps({'tags': tags_to_return})
    return Response(response=payload, mimetype="application/json")


@app.route('/podcasts', methods=['DELETE'])
def delete_podcasts():
    """ Delete all podcasts """
    db.podcasts.remove()
    payload = dumps({})
    return Response(response=payload, status=204, mimetype="application/json")


@app.route('/podcasts')
def get_podcasts():
    """ Get all podcasts """
    podcasts = db.podcasts.find()

    # Get users tags
    users_tags = list(db.user_tags.find())
    users_tags = [tag['label'] for tag in users_tags]

    # Filter by podcast containing users tags
    podcast_to_return = []
    for podcast in podcasts:
        tag_ok = False
        for tag in podcast['tags']:
            if tag in users_tags:
                tag_ok = True
        if tag_ok:
            podcast_to_return.append(podcast)

    payload = dumps({'podcasts': podcast_to_return})
    return Response(response=payload, mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)
