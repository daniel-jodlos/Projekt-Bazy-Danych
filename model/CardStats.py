from datetime import timedelta, datetime
from mongoengine import *
from model.Card import Card

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


class CardStats(EmbeddedDocument):
    card = EmbeddedDocumentField(Card)
    history = ListField(IntField, default=[])
    scheduled_for = DateTimeField(null=True)

    def __str__(self):
        return str(self.card)

    def was_seen(self):
        return len(self.history) > 0

    def is_learnt(self):
        return len(self.history) >= 2 and self.history[0][1] != "Źle" and self.history[1][1] != "Źle"

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




