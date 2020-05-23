from mongoengine import *

class Card(EmbeddedDocument):
    question = StringField(max_length=100)
    answer = StringField(max_length=200)

    def __str__(self):
        return "%s:\n----------------------------\n%s\n\n" % (self.question, self.answer)