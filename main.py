import curses
import random

from model import Deck
from model.User import *
from ui import choice_window, show_question, deck_edit_screen, study_deck


# deck_edit_screen(stdscr, DeckCreationWizard(user, chosen_deck))

def show_menu(stdscr, deck: Deck, user: User):
    options = ['study', 'delete', 'edit', 'cancel']
    choice = options[choice_window(deck.name, options, stdscr)]

    if choice == 'delete':
        pass
    elif choice == 'edit':
        deck_edit_screen(stdscr, DeckCreationWizard(user, deck))
        user.save()
    elif choice == 'study':
        study_deck(stdscr, deck, user)
    elif choice == 'cancel':
        pass


def main(stdscr):
    stdscr.keypad(True)
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.noecho()

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

    while True:
        choice = choice_window('Talie', user.get_decks_names(), stdscr)
        deck = list(user.decks)[choice]
        show_menu(stdscr, deck, user)

    user.save()


curses.wrapper(main)
