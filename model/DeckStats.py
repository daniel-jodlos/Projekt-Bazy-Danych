from mongoengine import *
from model.CardStats import *


class DeckStats(EmbeddedDocument):
    deck = LazyReferenceField(Deck)
    deck_name = StringField()
    stats = EmbeddedDocumentListField(CardStats)
    unseen = EmbeddedDocumentListField(Card)

    def get_first_n_unseen(self, n):
        array = [CardStats(card=a) for a in self.unseen[0:(n - 1)]]
        self.unseen = self.unseen[n:]
        self.stats += array
        return array

    def get_scheduled_for_today(self, n):
        self.stats.filter()