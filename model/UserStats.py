from mongoengine import *
from model.CardStats import User
from model.DeckStats import *


class UserStats(Document):
    user = ReferenceField(User)
    deck_stats = EmbeddedDocumentListField(DeckStats)

    def import_deck(self, deck):
        s = DeckStats(deck=deck, deck_name=deck.name, stats=[], unseen=deck.cards)
        self.deck_stats.append(s)
        self.save()
