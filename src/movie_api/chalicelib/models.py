from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class User:
    username: str
    password: str
    email_address: str
    first_name: str
    last_name: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Movie:
    _id: str = field(init=False)
    title: str = field(init=False)
    description: str = field(init=False)
    userId: str = field(init=False)
    director: str = field(init=False)
    imdbid: str = field(init=False)
    favorite: bool = field(init=False)
    year: Optional[str] = field(init=False)
    runtime: Optional[str] = field(init=False)
    genres: Optional[str] = field(init=False)
    writer: Optional[str] = field(init=False)
    actors: Optional[str] = field(init=False)
    plot: Optional[str] = field(init=False)
    poster: Optional[str] = field(init=False)
    wishlist: bool = field(init=False)
    format: str = field(init=False)
    rating: Optional[int] = field(init=False)

    # this.UserId = response.movie.userId;
    # this.Wishlist = response.movie.wishlist;
    # this.Format = response.movie.format;
    # this.Rating = response.movie.rating;
    # this.Title = response.movie.title;
    # this.Director = response.movie.director;
    @classmethod
    def create_from_db(cls, db_movie):
        movie = cls()
        movie.userId = db_movie["userId"]
        movie.wishlist = db_movie["wishlist"]
        movie.format = db_movie["format"]
        movie.rating = db_movie["rating"]
        movie.title = db_movie["title"]
        movie.director = db_movie["director"]
        return movie.to_dict()
