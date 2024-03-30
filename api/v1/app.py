#!/usr/bin/python3
""" main api file """

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = int(getenv('HBNB_API_PORT', '5000'))

app.register_blueprint(app_views)

@app.teardown_appcontext
def reset(exeption):
    """ reload objects from storage """
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
