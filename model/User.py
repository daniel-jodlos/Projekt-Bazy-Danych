from model.UserStats import UserStats
from mongoengine import *


class User(Document):
    username = StringField(max_length=20)
    email = EmailField(max_length=40)
    userStats = ReferenceField(UserStats)

    def __str__(self):
        return "%s (%s)" % (self.username, self.email)

    def get_stats(self):
        return self.userStats