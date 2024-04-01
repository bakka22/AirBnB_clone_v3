#!/usr/bin/python3
""" handels default RESTFul API actions for Amenitys """

from flask import abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Retrievs a list of all amenities """
    all_amenities = storage.all(Amenity)
    list_of_amenities = list(all_amenities.values())
    list_of_amenities = [amenity.to_dict() for amenity in list_of_amenities]
    return json.dumps(list_of_amenities, indent=3)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id):
    """ Retrievs a Amenity object """
    if type(amenity_id) != str:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return json.dumps(amenity.to_dict(), indent=3)
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete a amenity by id """
    if type(amenity_id) != str:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return json.dumps({}, indent=3), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """ adds a new amenity """
    try:
        new_st = request.get_json()
        if new_st.get("name") is None:
            return "Missing name", 400
        new_obj = Amenity(**new_st)
        new_obj.save()
        return json.dumps(new_obj.to_dict(), indent=3), 201
    except Exception:
        return "Not a JSON", 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ updates a amenity """
    if type(amenity_id) != str:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        new_attr = request.get_json()
        for key, value in new_attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                amenity.__dict__[key] = value
        dic = amenity.to_dict()
        storage.delete(amenity)
        new = Amenity(**dic)
        new.save()
        return json.dumps(new.to_dict(), indent=3), 200
    except Exception:
        return "Not a JSON", 400
