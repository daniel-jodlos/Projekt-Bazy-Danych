from mongoengine import *
from datetime import datetime, timedelta


UNSEEN = 0
SEEN = 1
LEARNT = 2

FEEDBACK_SETTINGS = {
    UNSEEN: {
        "Źle": timedelta(seconds=10 * 60),
        "Dobrze": timedelta(days=1)
    },
    SEEN: {
        "Źle": timedelta(seconds=60 * 10),
        "Trudne": timedelta(days=1),
        "Dobrze": timedelta(days=2),
        "Łatwe": timedelta(days=4)
    },
    LEARNT: {
        "Źle": timedelta(seconds=60 * 10),
        "Trudne": timedelta(days=1),
        "Dobrze": timedelta(days=7),
        "Łatwe": timedelta(days=14)
    }
}


class SharedCard(EmbeddedDocument):
    dc_id = IntField(required=True)
    question = StringField(max_length=100, required=True)
    answer = StringField(max_length=200, required=True)

    meta = {'allow_inheritance': True}

    def __str__(self):
        return '{}) {} -> {}'.format(self.dc_id, self.question, self.answer)

    def set_dc_id(self, new_id):
        self.dc_id = new_id


class HistoryEntry(EmbeddedDocument):
    state = IntField(required=True)
    answer = StringField(max_length=30, required=True)


class PrivateCard(SharedCard):
    history = EmbeddedDocumentListField(HistoryEntry, default=[])
    scheduled_for = DateTimeField(null=True)
    state = IntField(default=UNSEEN)

    def was_seen(self):
        return self.state == SEEN or self.state == LEARNT

    def is_learnt(self):
        return len(self.history) >= 2 and self.history[0] != "Źle" and self.history[1] != "Źle"

    def _get_state(self):
        return self.state

    def set_answer(self, answer):
        self.history.append(HistoryEntry(state=self._get_state(), answer=answer))
        self.scheduled_for = datetime.now() + FEEDBACK_SETTINGS[self._get_state()][answer]

        if self.state == UNSEEN:
            self.state = SEEN
        if len(self.history) >= 2 and self.history[0].answer != "Źle" and self.history[1].answer != "Źle":
            self.state = LEARNT
        if answer == 'Źle':
            self.state = SEEN

    def get_shared_card(self):
        return SharedCard(self)

    def get_possible_answers(self):
        return list(FEEDBACK_SETTINGS[self._get_state()].keys())
