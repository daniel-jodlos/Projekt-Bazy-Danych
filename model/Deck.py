from mongoengine import *
from model.Card import *
from datetime import datetime, date
from math import inf


class SharedDeck(Document):
    cards = EmbeddedDocumentListField(SharedCard, required=True, null=False)
    author_id = ObjectIdField(required=True)
    author_name = StringField(max_length=100, required=True)
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000)
    created = DateTimeField(default=datetime.now())

    def __str__(self):
        return '{name} by {author}'.format(name=self.name, author=self.author_name)


class PrivateDeck(EmbeddedDocument):
    cards = EmbeddedDocumentListField(PrivateCard, default=[])
    name = StringField(max_length=100)
    size = IntField(default=0)

    def __str__(self):
        return self.name

    def add_card(self, card):
        card.set_dc_id(self.size)
        self.size += 1
        self.cards.append(card)

    def to_csv(self, filename):
        with open(filename, "w+") as file:
            file.write("question;answer\n")
            file.writelines("%s;%s\n" % (a.question, a.answer) for a in self.cards)

    def share(self, user, description):
        shared = SharedDeck(cards=[c.get_shared_card() for c in self.cards], name=self.name, description=description,
                            author_name=user.username, author_id=user.id)
        shared.save()
        return shared

    def get_unseen_cards(self, max_cards):
        res = self.cards.filter(state=UNSEEN)
        return res if len(res) <= max_cards else res[:max_cards]

    def get_seen_for_today(self, max_cards=inf):
        result = []
        for card in self.cards:
            if len(result) == max_cards:
                break
            elif card.state == UNSEEN:
                continue
            elif card.scheduled_for is not None and card.for_today():
                result.append(card)

        return result

    def get_cards_package_for_today(self, size):
        res = self.get_seen_for_today(size)
        if len(res) < size:
            res += self.get_unseen_cards(size - len(res))

        return res
