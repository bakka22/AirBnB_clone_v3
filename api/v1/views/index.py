#!/usr/bin/python3
""" return the status of the api """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def index():
    return jsonify({"status": "OK"})
