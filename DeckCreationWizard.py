from model.Card import PrivateCard
from pandas import read_csv


class DeckCreationWizard(object):
    def __init__(self, author, deck):
        self.author = author
        self.deck = deck

    def save(self, exception=False):
        try:
            self.author.save()
        except Exception:
            if exception:
                raise

    def add_card(self, c: PrivateCard):
        self.deck.add_card(c)
        self.save()

    def new_card(self):
        d = PrivateCard(question='', answer='')
        self.add_card(d)
        return d
        
    def set_name(self, name: str):
        self.deck.name = name

    def delete_card(self, index):
        del self.cards[index]
        for i, c in enumerate(self.cards):
            c.dc_id = i
        self.save()

    @property
    def name(self):
        return self.deck.name

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

    def share(self):
        self.deck.share()
        
    def __del__(self):
        self.save(exception=True)
