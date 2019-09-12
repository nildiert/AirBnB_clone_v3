#!/usr/bin/python3
"""
Places file
"""

import models
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Create and returns a new a new place with the status code 201
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    city = storage.get("City", city_id)
    user = storage.get("User", id=request.json['user_id'])
    if city and user:
        request.json['city_id'] = city_id
        place = models.place.Place(**request.json)
        place.save()
        return jsonify(place.to_dict()), 201
    abort(404)

@app_views.route('places/<place_id>')
def get_place(place_id):
    """
    Retrieve a Place object by id
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('cities/<city_id>/places')
def get_places(city_id):
    """
    Retrieves the list of all Place objects of city
    """
    places = []
    city = storage.get("City", city_id)
    if city:
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    abort(404)
