#!/usr/bin/python3
""" handels default RESTFul API actions for States """

from flask import abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrievs a list of all states """
    all_states = storage.all(State)
    list_of_states = list(all_states.values())
    list_of_states = [state.to_dict() for state in list_of_states]
    return json.dumps(list_of_states, indent=3)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    """ Retrievs a State object """
    if type(state_id) != str:
        abort(404)
    state = storage.get(State, state_id)
    if state:
        return json.dumps(state.to_dict(), indent=3)
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a state by id """
    if type(state_id) != str:
        abort(404)
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return json.dumps({}, indent=3), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """ adds a new state """
    try:
        new_st = request.get_json()
        if new_st.get("name") is None:
            return "Missing name", 400
        new_obj = State(**new_st)
        new_obj.save()
        return json.dumps(new_obj.to_dict(), indent=3), 201
    except Exception:
        return f"Not a JSON", 400


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates a state """
    if type(state_id) != str:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        new_attr = request.get_json()
        for key, value in new_attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                state.__dict__[key] = value
        dic = state.to_dict()
        storage.delete(state)
        new = State(**dic)
        new.save()
        return json.dumps(new.to_dict(), indent=3), 200
    except Exception:
        return f"Not a JSON", 400
