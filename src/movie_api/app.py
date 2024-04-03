import os
from dataclasses import dataclass, field
from typing import Optional

import certifi
import pymongo
from chalice import Chalice
from dataclasses_json import dataclass_json, LetterCase
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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Movie:
    _id: str = field(default=None)
    title: str = field(default=None)
    description: str = field(default=None)
    userId: str = field(default=None)
    director: str = field(default=None)
    imdbid: str = field(default=None)
    wishlist: bool = field(default=False)
    format: str = field(default=None)
    rating: int = field(default=0)
    favorite: bool = field(init=False, default=False)
    year: Optional[str] = field(init=False, default=None)
    runtime: Optional[str] = field(init=False, default=None)
    genres: Optional[str] = field(init=False, default=None)
    writer: Optional[str] = field(init=False, default=None)
    actors: Optional[str] = field(init=False, default=None)
    plot: Optional[str] = field(init=False, default=None)
    poster: Optional[str] = field(init=False, default=None)

    @classmethod
    def create_from_db(cls, db_movie):
        cls(
            str(db_movie['_id']),
            db_movie["title"],
            db_movie["description"],
            db_movie["userId"],
            db_movie["director"],
            db_movie['imdbid'],
            db_movie["wishlist"],
            db_movie["format"],
            db_movie["rating"],
        ).to_dict()


def get_client():
    return pymongo.MongoClient(os.environ['CONNECTION_STRING'], tlsCAFile=certifi.where())


def find_movie(user_id, imdb_id):
    client = get_client()
    try:
        db_movie = client.ohgnarly.Movies.find_one({'userId': user_id, 'imdbid': imdb_id})
        return Movie.create_from_db(db_movie)
    finally:
        client.close()


def find_movies(user_id):
    client = get_client()
    try:
        db_movies_cursor = client.ohgnarly.Movies.find({'userId': user_id})
        return list(map(Movie.create_from_db, db_movies_cursor))
    finally:
        client.close()


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

