#!/usr/bin/python3
""" handels default RESTFul API actions for Places """

from flask import abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
import json


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ Retrievs a list of all reviews """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_reviews = place.reviews
    all_reviews = [review.to_dict() for review in all_reviews]
    return json.dumps(all_reviews, indent=3)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrievs a Review object """
    if type(review_id) != str:
        abort(404)
    review = storage.get(Review, review_id)
    if review:
        return json.dumps(review.to_dict(), indent=3)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ delete a review by id """
    if type(review_id) != str:
        abort(404)
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return json.dumps({}, indent=3), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """ adds a new review """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        new = request.get_json()
        if new.get("name") is None:
            return "Missing name", 400
        new['place_id'] = place_id
        new_review = Review(**new)
        new_review.save()
        return json.dumps(new_review.to_dict(), indent=3), 201
    except Exception as e:
        return "Not a JSON {e}", 400


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates a review """
    if type(review_id) != str:
        abort(404)
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        new_attr = request.get_json()
        for key, value in new_attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                review.__dict__[key] = value
        new = review.to_dict()
        storage.delete(review)
        new = Review(**new)
        new.save()
        return json.dumps(new.to_dict(), indent=3), 200
    except Exception:
        return "Not a JSON", 400
