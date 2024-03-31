from src.movie_api.app import get_movie


def test_get_movie():
    print(get_movie('5d9ce112b3608e16726bc0ea', 'tt0468569'))
