from src.movie_api.app import get_formats
from imdb import Cinemagoer

imdb_api = Cinemagoer()
imdb_api.get_movie('')


def test_get_formats():
    print((get_formats()))
