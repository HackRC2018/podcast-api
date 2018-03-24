import functools
import os
import re
import pymongo

from flask import Flask
from flask import jsonify

app = Flask(__name__)

# DB Config
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)
MONGODB_DB = os.environ.get('MONGODB_DB', 'podcast')


mongo_client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = mongo_client[MONGODB_DB]


@app.route('/tags')
def get_tags():
    s = ['data1', 'data2']
    return jsonify(list(s))


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)
