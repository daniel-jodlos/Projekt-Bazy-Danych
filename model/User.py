from mongoengine import *
import hashlib

from DeckCreationWizard import DeckCreationWizard
from model.Deck import PrivateDeck, SharedDeck, PrivateCard


class NoSuchUserException(Exception):
    def __init__(self):
        super()


class IncorrectPasswordException(Exception):
    def __init__(self):
        super()


class User(Document):
    username = StringField(max_length=20)
    password_hash = StringField(max_length=256, required=True)
    email = EmailField(max_length=40, required=True, unique=True)
    decks = EmbeddedDocumentListField(PrivateDeck, default=[])

    def __str__(self):
        return "%s (%s)" % (self.username, self.email)

    def get_decks_names(self):
        return [d.name for d in self.decks]

    def import_deck(self, deck: SharedDeck):
        self.decks.append(PrivateDeck(name=deck.name,
                                      cards=[PrivateCard(question=c.question, answer=c.answer, dc_id=c.dc_id) for c in
                                             deck.cards]))
        self.cascade_save()

    def create_new_deck(self, name: str) -> DeckCreationWizard:
        deck = self.decks.create(name=name)
        self.save()
        return DeckCreationWizard(self, deck)

    def drop_deck(self, index):
        del self.decks[index]
        self.save()


def login_user(email, password):
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User.objects(email=email)[0]
        if user.password_hash == password_hash:
            return user
        raise IncorrectPasswordException()
    except IndexError:
        raise NoSuchUserException()


def register_user(username, email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return User(username=username, email=email, password_hash=password_hash).save()


def find_by_id(uid):
    return User.objects(id=uid)
