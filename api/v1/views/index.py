#!/usr/bin/python3
""" api blueprint """

from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
import json

classes = {"states": State, "cities": City, "amenities": Amenity,
           "reviews": Review, "places": Place, "users": User}


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def index():
    """ return status of the api """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def count():
    """ return the number of each module """
    dic = {}
    for key, cls in classes.items():
        dic[key] = storage.count(cls)
    return json.dumps(dic, indent=3)
