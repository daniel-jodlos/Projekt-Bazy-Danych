from mongoengine import *

from DeckCreationWizard import DeckCreationWizard
from model.Deck import PrivateDeck, SharedDeck, PrivateCard


class User(Document):
    username = StringField(max_length=20)
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


