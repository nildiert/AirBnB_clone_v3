#!/usr/bin/python3
"""
Places file
"""

import models
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from os import getenv


@app_views.route('places/<place_id>/amenities')
def get_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    amenities = []
    place = storage.get("Place", place_id)
    if place:
        for review in place.amenities:
            amenities.append(review.to_dict())
        return jsonify(amenities)
    abort(404)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'])
def delete_amenity_on_place(place_id, amenity_id):
    """
    Deletes Amenity instance on Place
    """
    place = storage.get("Place", id=place_id)
    amenity = storage.get("Amenity", id=amenity_id)
    if place and amenity:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place_amenities = place.amenities
            if amenity not in place_amenities:
                abort(404)
            place_amenities.remove(amenity)
        else:
            place_amenities = place.amenity_ids
            if amenity_id not in place_amenities:
                abort(404)
            place_amenities.remove(amenity_id)
        place.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=['POST'])
def set_amenity_on_place(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    place = storage.get("Place", id=place_id)
    amenity = storage.get("Amenity", id=amenity_id)
    if place and amenity:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place_amenities = place.amenities
            if amenity in place_amenities:
                return jsonify(amenity.to_dict()), 200
            place_amenities.append(amenity)
        else:
            place_amenities = place.amenity_ids
            if amenity_id in place_amenities:
                return jsonify(amenity.to_dict()), 200
            place_amenities.append(amenity_id)
        place.save()
        return jsonify(amenity.to_dict()), 201
    abort(404)
