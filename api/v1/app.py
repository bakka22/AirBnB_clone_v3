#!/usr/bin/python3
""" main api file """

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = int(getenv('HBNB_API_PORT', '5000'))

app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def reset(exeption):
    """ reload objects from storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    ''' handles 404 error and gives json formatted response '''
    response = make_response(jsonify({'error': 'Not found'}), 404)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
