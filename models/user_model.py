import datetime
from dataclasses import dataclass


@dataclass
class UserModel:
    username: str
    email: str
    password: str


@dataclass
class UserModelOutput:
    user_id: str
    username: str
    email: str
    created_on: datetime.datetime
    last_login: datetime.datetime
    password: str

    def to_json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_on": self.created_on,
            "last_login": self.last_login if self.last_login else None,
        }
