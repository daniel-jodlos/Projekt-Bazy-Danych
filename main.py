import datetime
from pandas import read_csv

class Card:

    question = None
    answer = None
    lastSeen = None
    seenCounter = 0
    seeIn = None

    def __init__(self, q, a):
        self.question = q
        self.answer = a

    def see(self):
        self.seenCounter += 1
        return self.question, self.answer

    def set_answer(self, answer):
        self.seenCounter += 1
        self.lastSeen = datetime.datetime.now()
        self.seeIn = datetime.datetime.now() + datetime.timedelta(seconds=10*60)

    def __str__(self):
        return "%s:\n----------------------------\n%s\n\n" % (self.question, self.answer)


class Deck(object):
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_next_card(self):
        return self.cards.pop(0)

    def load_csv(self, filename):
        df = read_csv(filename, sep=';')
        for (q, a) in zip(df['question'], df['answer']):
            self.add_card(Card(q, a))

    def to_csv(self, filename):
        with open(filename, "w+") as file:
            file.write("question;answer\n")
            file.writelines("%s;%s\n" % (a.question, a.answer) for a in self.cards)
