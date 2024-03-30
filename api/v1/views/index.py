#!/usr/bin/python3
""" return the status of the api """

from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.user import User
from models import engine

classes = {"states": State, "cities": City, "amenities": Amenity,
        "reviews": Review, "places": Place, "users": User}

@app_views.route('/status')
def index():
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def count():
    dic = {}
    for key, cls in classes.items():
        dic[key] = engine.count(cls)
    return jsonify(dic)

