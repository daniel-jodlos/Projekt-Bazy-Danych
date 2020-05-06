from datetime import timedelta, datetime
from pandas import read_csv
from mongoengine import *

connect("flashcards")

ANSWERS = {
    "new": {
        "Źle": timedelta(seconds=10 * 60),
        "Dobrze": timedelta(days=1)
    },
    "seen": {
        "Źle": timedelta(seconds=60 * 10),
        "Trudne": timedelta(days=1),
        "Dobrze": timedelta(days=2),
        "Łatwe": timedelta(days=4)
    },
    "learnt": {
        "Źle": timedelta(seconds=60 * 10),
        "Trudne": timedelta(days=1),
        "Dobrze": timedelta(days=7),
        "Łatwe": timedelta(days=14)
    }
}


class User(Document):
    username = StringField(max_length=20)
    email = EmailField(max_length=40)

    def __str__(self):
        return "%s (%s)" % (self.username, self.email)

    def get_stats(self):
        return UserStats.objects(user=self)[0]


class Card(EmbeddedDocument):
    question = StringField(max_length=100)
    answer = StringField(max_length=200)

    def __str__(self):
        return "%s:\n----------------------------\n%s\n\n" % (self.question, self.answer)


class Deck(Document):
    cards = EmbeddedDocumentListField(Card)
    author = ReferenceField(User)
    name = StringField(max_length=100)
    description = StringField(max_length=1000)

    def add_card(self, card):
        self.cards.append(card)

    def get_next_card(self):
        return self.cards.pop(0)

    def load_csv(self, filename):
        df = read_csv(filename, sep=';')
        for (q, a) in zip(df['question'], df['answer']):
            self.add_card(Card(question=q, answer=a))
        self.save()

    def to_csv(self, filename):
        with open(filename, "w+") as file:
            file.write("question;answer\n")
            file.writelines("%s;%s\n" % (a.question, a.answer) for a in self.cards)


class CardStats(EmbeddedDocument):
    card = EmbeddedDocumentField(Card)
    history = ListField(IntField, default=[])
    scheduled_for = DateTimeField(null=True)

    def __str__(self):
        return str(self.card)

    def was_seen(self):
        return len(self.history) > 0

    def is_learnt(self):
        return len(self.history) >= 2 and self.history[0][1] is not "Źle" and self.history[1][1] is not "Źle"

    def _get_state(self):
        if not self.was_seen():
            return "new"
        elif not self.is_learnt():
            return "seen"
        else:
            return "learnt"

    def set_answer(self, answer):
        self.history.append((self._get_state(), answer))
        self.scheduled_for = datetime.now() + ANSWERS[self._get_state()][answer]


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


class UserStats(Document):
    user = ReferenceField(User)
    deck_stats = EmbeddedDocumentListField(DeckStats)

    def import_deck(self, deck):
        s = DeckStats(deck=deck, deck_name=deck.name, stats=[], unseen=deck.cards)
        self.deck_stats.append(s)
        self.save()
