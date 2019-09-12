#!/usr/bin/python3
"""
Places file
"""

import models
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Create and returns a new a new review with the status code 201
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    place = storage.get("Place", place_id)
    user = storage.get("User", id=request.json['user_id'])
    if place and user:
        request.json['place_id'] = place_id
        review = models.review.Place(**request.json)
        review.save()
        return jsonify(review.to_dict()), 201
    abort(404)


@app_views.route('reviews/<review_id>')
def get_review(review_id):
    """
    Retrieves a Review object by id
    """
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('places/<place_id>/reviews')
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    reviews = []
    place = storage.get("Place", place_id)
    if place:
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a State instance
    """
    review = storage.get("Review", id=review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)
