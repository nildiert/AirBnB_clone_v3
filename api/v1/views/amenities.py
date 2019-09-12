#!/usr/bin/python3
"""
Amenities view
"""

import models
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/amenities')
def get_amenities():
    """
    Retrieves the list of all Amenities objects
    """
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object by id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
    Create a new Amenity instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    amenity = models.amenity.Amenity(name=request.json['name'])
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Update an amenity instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    amenity = storage.get("Amenity", id=amenity_id)
    if amenity:
        amenity.name = request.json['name']
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Delete a amenity instance
    """
    amenity = storage.get("Amenity", id=amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)
