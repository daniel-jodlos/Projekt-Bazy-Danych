import curses
import random

from model.User import *
from ui import choice_window, show_question, deck_edit_screen

try:
    user = login_user('danjod40@gmail.com')
    print("Logged in as", end=' ')
except Exception:
    print("Registered as", end=' ')
    user = register_user('danjod', 'danjod40@gmail.com')

if len(user.decks) < 3:
    deck_wizard = user.create_new_deck('random_deck_{}'.format(random.uniform(1, 10)))
    deck_wizard.load_csv('example.csv')
    deck_wizard.save()

stdscr = curses.initscr()
stdscr.keypad(True)
curses.cbreak()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.noecho()

choice = choice_window('Talie:', user.get_decks_names(), stdscr)
chosen_deck = user.decks[choice]

# for card in chosen_deck.get_cards_package_for_today(10):
#     answer = show_question(stdscr, card.question, card.answer, card.get_possible_answers())
#     card.set_answer(card.get_possible_answers()[answer])
#     user.save()

deck_edit_screen(stdscr, DeckCreationWizard(user, chosen_deck))

curses.endwin()
user.save()

# curses.wrapper(main)
