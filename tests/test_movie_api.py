from imdb import Cinemagoer
from imdb.Movie import Movie
from src.movie_api.app import get_movies

imdb_api = Cinemagoer()


def test_get_formats():
    get_movies('5d9ce112b3608e16726bc0ea')
