#!/usr/bin/python3
""" Flask app """

from models import storage
from flask import Flask
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_request(exception=None):
    storage.close()


if __name__ == "__main__":
    my_host = environ.get("HBNB_API_HOST")
    my_port = environ.get("HBNB_API_PORT")
    app.run(host=my_host, port=my_port, threaded=True)
