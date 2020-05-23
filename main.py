from math import ceil, floor

from model import *
import curses
import curses.textpad


def print_flashcard_question(fwindow, card):
    fwindow.clear()
    _, x = fwindow.getmaxyx()
    x = floor((x-len(card.question))/2)
    fwindow.addstr(0, x, card.question)
    fwindow.refresh()


def print_flashcard_answer(awindow, card):
    awindow.clear()
    _, x = awindow.getmaxyx()
    awindow.addstr(0, floor((x-len(card.answer))/2), card.answer)
    awindow.refresh()


def main(stdscr):
    stdscr.clear()
    y, x = stdscr.getmaxyx()
    ncols = x
    nlines = ceil(100/x)
    question_window = curses.newwin(nlines, ncols, 0, 0)
    answer_window = curses.newwin(ceil(200/x), ncols, nlines+1, 0)
    stdscr.refresh()
    deck = Deck.objects[0]
    curses.noecho()

    for card in deck.cards:
        answer_window.clear()
        stdscr.refresh()
        print_flashcard_question(question_window, card)
        stdscr.getch()
        print_flashcard_answer(answer_window, card)
        stdscr.refresh()
        stdscr.getch()

    stdscr.getch()


curses.wrapper(main)
