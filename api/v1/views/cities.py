#!/usr/bin/python3
""" handels default RESTFul API actions for States """

from flask import abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ Retrievs a list of all cities """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = state.cities
    all_cities = [city.to_dict() for city in all_cities]
    return json.dumps(all_cities, indent=3)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrievs a City object """
    if type(city_id) != str:
        abort(404)
    city = storage.get(City, city_id)
    if city:
        return json.dumps(city.to_dict(), indent=3)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ delete a city by id """
    if type(city_id) != str:
        abort(404)
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return json.dumps({}, indent=3), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def add_city(state_id):
    """ adds a new city """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        new = request.get_json()
        if new.get("name") is None:
            return "Missing name", 400
        new['state_id'] = state_id
        new_city = City(**new)
        new_city.save()
        return json.dumps(new_city.to_dict(), indent=3), 201
    except Exception as e:
        return f"Not a JSON {e}", 400


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates a city """
    if type(city_id) != str:
        abort(404)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        new_attr = request.get_json()
        for key, value in new_attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                city.__dict__[key] = value
        new = city.to_dict()
        storage.delete(city)
        new = City(**new)
        new.save()
        return json.dumps(new.to_dict(), indent=3), 200
    except Exception:
        return f"Not a JSON", 400
