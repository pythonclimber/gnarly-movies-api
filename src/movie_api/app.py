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
    _id: str = field(init=False)
    title: str = field(init=False)
    description: str = field(init=False)
    userId: str = field(init=False)
    director: str = field(init=False)
    imdbid: str = field(init=False)
    favorite: Optional[bool] = field(init=False, default=False)
    year: Optional[str] = field(init=False, default=None)
    runtime: Optional[str] = field(init=False, default=None)
    genres: Optional[str] = field(init=False, default=None)
    writer: Optional[str] = field(init=False, default=None)
    actors: Optional[str] = field(init=False, default=None)
    plot: Optional[str] = field(init=False, default=None)
    poster: Optional[str] = field(init=False, default=None)
    wishlist: bool = field(init=False, default=False)
    format: str = field(init=False, default=None)
    rating: Optional[int] = field(init=False)

    @classmethod
    def create_from_db(cls, db_movie):
        movie = cls()
        movie._id = str(db_movie['_id'])
        movie.userId = db_movie["userId"]
        movie.wishlist = db_movie["wishlist"]
        movie.format = db_movie["format"]
        movie.rating = db_movie["rating"]
        movie.title = db_movie["title"]
        movie.director = db_movie["director"]
        movie.description = db_movie["description"]
        movie.imdbid = db_movie['imdbid']
        return movie.to_dict()


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

