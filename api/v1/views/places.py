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


@app_views.route('places/<place_id>', methods=['PUT'])
def update_places(place_id):
    """
    Update a Place instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    place = storage.get("Place", place_id)
    if place:
        if 'name' in request.json.keys():
            place.name = request.json['name']
        if 'description' in request.json.keys():
            place.description = request.json['description']
        if 'number_rooms' in request.json.keys():
            place.number_rooms = request.json['number_rooms']
        if 'number_bathrooms' in request.json.keys():
            place.number_bathrooms = request.json['number_bathrooms']
        if 'max_guest' in request.json.keys():
            place.max_guest = request.json['max_guest']
        if 'price_by_night' in request.json.keys():
            place.price_by_night = request.json['price_by_night']
        if 'latitude' in request.json.keys():
            place.latitude = request.json['latitude']
        if 'longitude' in request.json.keys():
            place.longitude = request.json['longitude']
        place.save()
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route('places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Delete a Place instance
    """
    place = storage.get("Place", place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)
