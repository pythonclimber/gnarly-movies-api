import os

import certifi
import pymongo
from chalice import Chalice
from dotenv import load_dotenv, find_dotenv
from imdb import Cinemagoer

load_dotenv(find_dotenv())
app = Chalice(app_name='movie_api')
imdb_api = Cinemagoer()
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


class DbClient:
    _client = None

    @staticmethod
    def get_instance():
        if not DbClient._client:
            DbClient()

        return DbClient._client

    def __init__(self):
        if DbClient._client is not None:
            raise ValueError("This class is a singleton")
        else:
            DbClient._client = pymongo.MongoClient(os.environ['CONNECTION_STRING'], tlsCAFile=certifi.where())


def build_movie_response(db_movie):
    return {
        "_id": str(db_movie["_id"]),
        "title": db_movie["title"],
        "description": db_movie["description"],
        "userId": db_movie["userId"],
        "director": db_movie["director"],
        "imdbid": db_movie["imdbid"],
        "wishlist": db_movie["wishlist"],
        "format": db_movie["format"],
        "rating": db_movie["rating"],
    }


def find_movie(user_id, imdb_id):
    client = DbClient.get_instance()
    db_movie = client.ohgnarly.Movies.find_one({'userId': user_id, 'imdbid': imdb_id})
    print(type(db_movie))
    return build_movie_response(db_movie)


def find_movies(user_id):
    client = DbClient.get_instance()
    db_movies_cursor = client.ohgnarly.Movies.find({'userId': user_id})
    return list(map(build_movie_response, db_movies_cursor))


def find_movie_details(imdb_id):
    imdb_id = imdb_id.replace('tt', '') if imdb_id.startswith('tt') else imdb_id
    return imdb_api.get_movie(imdb_id)


@app.route('/movie/{user_id}/{imdb_id}', methods=['GET'])
def get_movie(user_id, imdb_id):
    return find_movie(user_id, imdb_id)


@app.route('/movies/{user_id}', methods=['GET'])
def get_movies(user_id):
    return find_movies(user_id)


@app.route('/movie-formats', methods=['GET'])
def get_formats():
    return list(formats.values())


@app.route('/movie-details/{imdb_id}', methods=['GET'])
def get_movie_details(imdb_id):
    return find_movie_details(imdb_id)

