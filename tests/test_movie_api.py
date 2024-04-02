from imdb import Cinemagoer

from src.movie_api.app import get_movie

imdb_api = Cinemagoer()


def test_get_formats():
    get_movie('5d9ce112b3608e16726bc0ea', 'tt0120737')
