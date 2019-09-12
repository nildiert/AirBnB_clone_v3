#!/usr/bin/python3
""" Index file """


import models
from models import storage
from flask import abort, jsonify
from api.v1.views import app_views


@app_views.route('/states')
def get_states():
    """
    Retrieves the list of all State objects
    """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """
    Retrieves a State object
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state)
    abort(404)
