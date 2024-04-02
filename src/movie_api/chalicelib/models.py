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
