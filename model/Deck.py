from mongoengine import *
from pandas import read_csv
from model.Card import Card
from model.User import User


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