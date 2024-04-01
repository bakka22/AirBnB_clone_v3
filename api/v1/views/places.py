#!/usr/bin/python3
""" handels default RESTFul API actions for Citys """

from flask import abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrievs a list of all places """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = city.places
    all_places = [place.to_dict() for place in all_places]
    return json.dumps(all_places, indent=3)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrievs a Place object """
    if type(place_id) != str:
        abort(404)
    place = storage.get(Place, place_id)
    if place:
        return json.dumps(place.to_dict(), indent=3)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete a place by id """
    if type(place_id) != str:
        abort(404)
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return json.dumps({}, indent=3), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """ adds a new place """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        new = request.get_json()
    except Exception:
        return "Not a JSON", 400
    u_id = new.get("user_id")
    if u_id is None:
        return "Missing user_id", 400
    usr = storage.get(User, u_id)
    if not usr:
        abort(404)
    if new.get("name") is None:
        return "Missing name", 400
    new['city_id'] = city_id
    new_place = Place(**new)
    new_place.save()
    return json.dumps(new_place.to_dict(), indent=3), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates a place """
    if type(place_id) != str:
        abort(404)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        new_attr = request.get_json()
        for key, value in new_attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                place.__dict__[key] = value
        new = place.to_dict()
        storage.delete(place)
        new = Place(**new)
        new.save()
        return json.dumps(new.to_dict(), indent=3), 200
    except Exception:
        return "Not a JSON", 400
