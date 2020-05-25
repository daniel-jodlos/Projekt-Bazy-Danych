import curses
import random

from model import Deck
from model.User import *
from ui import choice_window, show_question, deck_edit_screen, study_deck, get_user_input


# deck_edit_screen(stdscr, DeckCreationWizard(user, chosen_deck))

def show_menu(stdscr, deck_i: int, user: User):
    deck = list(user.decks)[deck_i]
    options = ['study',  'edit', 'share', 'delete', 'cancel']
    choice = options[choice_window(deck.name, options, stdscr)]

    if choice == 'delete':
        user.drop_deck(deck_i)
    elif choice == 'edit':
        deck_edit_screen(stdscr, DeckCreationWizard(user, deck))
        user.save()
    elif choice == 'study':
        study_deck(stdscr, deck, user)
    elif choice == 'cancel':
        pass
    elif choice == 'share':
        decription = get_user_input(stdscr, "{} deck description".format(deck.name))
        deck.share(user, decription)


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
        choice = choice_window('Talie', user.get_decks_names(), stdscr, {'n': -10})
        if choice >= 0:
            show_menu(stdscr, choice, user)
        elif choice == -10:
            name = get_user_input(stdscr, 'Nazwa nowej talii')
            deck_edit_screen(stdscr, user.create_new_deck(name))
            user.save()
        else:
            break

    user.save()


curses.wrapper(main)
