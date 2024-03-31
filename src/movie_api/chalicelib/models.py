from dataclasses import dataclass
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
    _id: str
    title: str
    description: str
    userId: str
    director: str
    imdbid: str
    favorite: bool
    year: Optional[str]
    runtime: Optional[str]
    genres: Optional[str]
    writer: Optional[str]
    actors: Optional[str]
    plot: Optional[str]
    poster: Optional[str]
    wishlist: bool
    format: str
    rating: Optional[int]