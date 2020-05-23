from model.Card import PrivateCard
from pandas import read_csv


class DeckCreationWizard(object):
    def __init__(self, author, deck):
        self.author = author
        self.deck = deck

    def save(self):
        self.author.save()

    def add_card(self, c: PrivateCard):
        print("Adding card: {}".format(c))
        self.deck.add_card(c)
        
    def set_name(self, name: str):
        self.deck.name = name

    @property
    def cards(self):
        return self.deck.cards

    @property
    def size(self):
        return self.deck.size

    def load_csv(self, filename):
        df = read_csv(filename, sep=';')
        for (q, a) in zip(df['question'], df['answer']):
            self.add_card(PrivateCard(question=q, answer=a))
        
    def __del__(self):
        self.save()
