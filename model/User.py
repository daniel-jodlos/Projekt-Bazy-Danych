from model.Deck import PrivateDeck, SharedDeck
from mongoengine import *
from DeckCreationWizard import DeckCreationWizard


def login_user(email):
    try:
        return User.objects(email=email)[0]
    except IndexError:
        raise Exception("No such user! Please register")


def register_user(username, email):
    return User(username=username, email=email).save()


def find_by_id(uid):
    return User.objects(id=uid)


class User(Document):
    username = StringField(max_length=20)
    email = EmailField(max_length=40)
    decks = EmbeddedDocumentListField(PrivateDeck, default=[])

    def __str__(self):
        return "%s (%s)" % (self.username, self.email)

    def get_decks_names(self):
        return [d.name for d in self.decks]

    def import_deck(self, deck: SharedDeck):
        self.decks.append(PrivateDeck(deck))
        self.cascade_save()

    def create_new_deck(self, name: str) -> DeckCreationWizard:
        deck = self.decks.create(name=name)
        self.save()
        return DeckCreationWizard(self, deck)
