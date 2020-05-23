from mongoengine import *
from model.CardStats import *
from model.Card import Card


class DeckStats(EmbeddedDocument):
    deck_id = ObjectIdField()
    deck_name = StringField()
    seen_stats = EmbeddedDocumentListField(CardStats)
    unseen = EmbeddedDocumentListField(Card)

    def get_first_n_unseen(self, n):
        array = [CardStats(card=a) for a in self.unseen[0:(n - 1)]]
        self.unseen = self.unseen[n:]
        self.seen_stats += array
        return array

    def get_scheduled_for_today(self, n):
        self.seen_stats.filter()