#!/usr/bin/python3
"""
Cities view
"""

import models
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities')
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    cities = []
    state = storage.get("State", state_id)
    if state:
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>')
def get_city(city_id):
    """
    Retrieve a City object by id
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/states/<states_id>/cities', methods=['POST'])
def create_city(states_id):
    """
    Create and returns a new city with the status code 201
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    state = storage.get("State", states_id)
    if state:
        city = models.city.City(name=request.json['name'], state_id=states_id)
        city.save()
        return jsonify(city.to_dict()), 201
    abort(404)


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Update a City instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    city = storage.get("City", id=city_id)
    if city:
        city.name = request.json['name']
        city.save()
        return jsonify(city.to_dict()), 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Delete a City object by id
    """
    city = storage.get("City", id=city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)
