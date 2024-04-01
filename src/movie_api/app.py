import json
import os

import certifi
import pymongo
from bson import json_util
from chalice import Chalice
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Chalice(app_name='movie_api')
formats = {
    'DVD': 'DVD',
    'Bluray': 'Blu-ray',
    'Bluray3d': 'Blu-ray 3D',
    'Bluray4k': 'Blu-ray 4K',
    'DigitalSd': 'Digital SD',
    'DigitalHd': 'Digital HD',
    'DigitalUhd': 'Digital UHD',
    'VHS': 'VHS'
}


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
    return json_util.dumps(get_movies(user_id))


@app.route('/movie-formats', methods=['GET'])
def get_formats():
    return list(formats.values())
