import flask
from flask import Flask, request, redirect, make_response
from flask_cors import CORS
import json
import sys
import codecs
import logging
import urllib
import config

# Python2.x: Make default encoding as UTF-8
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('UTF8')


logging.basicConfig(filename='error.log', level=logging.DEBUG)
app = Flask(__name__)
app.config.from_object('config')
CORS(app)


@app.route('/')
def heart_beat():
    return flask.jsonify({"status": "ok"})


@app.route('/api/v1/stack_license', methods=['POST'])
def stack_license():
    input_json = request.get_json()
    #Need to change this
    response = { "stack_license": "Apache 2.0",
        "outlier_license": [
            {
                "pkg1-ver1": "license",
                "pkg2-ver2": "license"
            }],
        "conflict_license": [
            {
            "pkg1-ver1": "license",
            "pkg1-ver2": "license"
            }]
    }

    return flask.jsonify(response)


if __name__ == "__main__":
    app.run()
