import json
import os

import certifi
import pymongo
from bson import json_util
from chalice import Chalice
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Chalice(app_name='movie_api')


def get_client():
    return pymongo.MongoClient(os.environ['CONNECTION_STRING'], tlsCAFile=certifi.where())


def find_movie(user_id, imdb_id):
    client = get_client()
    try:
        return client.ohgnarly.Movies.find_one({'userId': user_id, 'imdbid': imdb_id})
    finally:
        client.close()


def find_movies(user_id):
    client = get_client()
    try:
        return list(client.ohgnarly.Movies.find({'userId': user_id}))
    finally:
        client.close()


@app.route('/movie/{user_id}/{imdb_id}', methods=['GET'])
def get_movie(user_id, imdb_id):
    return json.loads(json_util.dumps(get_movie(user_id, imdb_id)))


@app.route('/movies/{user_id}', methods=['GET'])
def get_movies(user_id):
    return json.loads(json_util.dumps(get_movies(user_id)))


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
