from math import ceil, floor
import curses
import curses.textpad
from model.User import *

try:
    user = login_user('danjod40@gmail.com')
    print("Logged in as", end=' ')
except Exception:
    print("Registered as", end=' ')
    user = register_user('danjod', 'danjod40@gmail.com')
print('{user}\n\nYour decks:'.format(user=user))

if len(user.decks) == 0:
    deck_wizard = user.create_new_deck('random_deck')
    deck_wizard.load_csv('example.csv')
    deck_wizard.save()

for deck in user.decks:
    print('- {}'.format(deck))

choice = int(input('\n\nWhich one do you choose in range[0-{}]? '.format(len(user.decks) - 1)))
chosen_deck = user.decks[choice]

for card in chosen_deck.get_cards_package_for_today(10):
    print('{}'.format(card.question))
    print('\nPossible answers:\n - {}\n'.format('\n - '.join(card.get_possible_answers())))
    card.set_answer(list(card.get_possible_answers())[1])

user.save()

# curses.wrapper(main)
