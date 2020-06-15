import hashlib

from mongoengine import *
from .User import User


class LoginCredentials(Document):
    password_hash = StringField(max_length=256, required=True)
    email = EmailField(max_length=40, required=True, unique=True)
    user = ReferenceField(User)

    def get_user(self):
        return self.user


class NoSuchUserException(Exception):
    def __init__(self):
        super()


class IncorrectPasswordException(Exception):
    def __init__(self):
        super()


def login_user(email, password):
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        credentials = LoginCredentials.objects(email=email)[0]
        if credentials.password_hash == password_hash:
            return credentials.get_user()
        raise IncorrectPasswordException()
    except IndexError:
        raise NoSuchUserException()


def register_user(username, email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = User(username=username, email=email)
    user.save()
    credentials = LoginCredentials(user=user, email=email, password_hash=password_hash)
    credentials.save()
    return user


def find_by_id(uid):
    return User.objects(id=uid)
