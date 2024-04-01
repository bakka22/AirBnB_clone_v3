#!/usr/bin/python3
""" handels default RESTFul API actions for Users """

from flask import abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
import json


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrievs a list of all users """
    all_users = storage.all(User)
    list_of_users = list(all_users.values())
    list_of_users = [user.to_dict() for user in list_of_users]
    return json.dumps(list_of_users, indent=3)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id):
    """ Retrievs a User object """
    if type(user_id) != str:
        abort(404)
    user = storage.get(User, user_id)
    if user:
        return json.dumps(user.to_dict(), indent=3)
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ delete a user by id """
    if type(user_id) != str:
        abort(404)
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return json.dumps({}, indent=3), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """ adds a new user """
    try:
        new_st = request.get_json()
        if new_st.get("email") is None:
            return "Missing email", 400
        if new_st.get("password") is None:
            return "Missing password", 400
        new_obj = User(**new_st)
        new_obj.save()
        return json.dumps(new_obj.to_dict(), indent=3), 201
    except Exception as e:
        return "Not a JSON {e}", 400


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ updates a user """
    if type(user_id) != str:
        abort(404)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        new_attr = request.get_json()
        for key, value in new_attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                user.__dict__[key] = value
        dic = user.to_dict()
        storage.delete(user)
        new = User(**dic)
        new.save()
        return json.dumps(new.to_dict(), indent=3), 200
    except Exception:
        return "Not a JSON", 400
