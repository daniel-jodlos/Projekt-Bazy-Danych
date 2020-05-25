import curses
from math import floor, ceil
import curses.textpad
import curses.ascii
from DeckCreationWizard import DeckCreationWizard


def centered_text(window, row, text, colour=None):
    _, x = window.getmaxyx()
    center = max(floor((x - len(text)) / 2), 0)

    if colour is None:
        window.addstr(row, center, text)
    else:
        window.addstr(row, center, text, colour)
    window.refresh()


def evenly_spaced_windows(amount, start_row, height, total_width):
    win_width = floor(total_width / amount)
    return [curses.newwin(height, win_width, start_row, win_width * i) for i in range(0, amount)]


def handle_key(textbox, key):
    y, x = textbox.win.getyx()

    if key == 27:
        return curses.ascii.BEL  # user pressed esc
    elif key == curses.KEY_HOME:
        textbox.win.move(y, 0)
    elif key in (curses.KEY_END, curses.KEY_RIGHT):
        msg_length = len(textbox.gather())
        textbox.win.move(y, x)  # reverts cursor movement during gather call

        if key == curses.KEY_END and msg_length > 0 and x < msg_length - 1:
            textbox.win.move(y, msg_length - 1)  # if we're in the content then move to the end
        elif key == curses.KEY_RIGHT and x < msg_length - 1:
            textbox.win.move(y, x + 1)  # only move cursor if there's content after it
    elif key == 410:
        # if we're resizing the display during text entry then cancel it
        # (otherwise the input field is filled with nonprintable characters)

        return curses.ascii.BEL
    else:
        return key


def get_input_window(stdscr, width, height, msg):
    stdscr.clear()
    y, x = stdscr.getmaxyx()
    win = curses.newwin(width, height, floor((y - height) / 2), floor((x - width) / 2))
    stdscr.addstr(floor((y - height) / 2) - 2, floor((x - width) / 2), '{}:'.format(msg), curses.color_pair(1))
    win.refresh()
    stdscr.refresh()

    textbox = curses.textpad.Textbox(win, insert_mode=True)
    return textbox.edit(lambda key: handle_key(textbox, key)).strip()


def edit_card(stdscr, card):
    y, x = stdscr.getmaxyx()
    MARGIN = 10
    new_q = get_input_window(stdscr, x - MARGIN, y - MARGIN, "Question (leave empty to pass, ESC to accept)")
    new_a = get_input_window(stdscr, x - MARGIN, y - MARGIN, "Answer (leave empty to pass, ESC to accept)")
    if new_q != '':
        card.question = new_q
    if new_a != '':
        card.answer = new_a


def choice_window(question, options: [], stdscr) -> int:
    stdscr.clear()

    y, x = stdscr.getmaxyx()
    centered_text(stdscr, floor((y - (2 + len(options))) / 2), question)

    win_x = max([len(i) for i in options]) + 3
    win_begin_y = floor((y - (2 + len(options))) / 2 + 2)
    win_begin_x = floor((x - win_x) / 2) - 3
    op_win = curses.newwin(len(options) + 1, win_x, win_begin_y, win_begin_x)
    op_win.refresh()
    stdscr.refresh()

    option = 0
    while True:
        for i, op in enumerate(options):
            if i == option:
                op_win.addstr(i, 0, '{pref} {value}'.format(pref='->' if i == option else '  ', value=op),
                              curses.color_pair(1))
            else:
                op_win.addstr(i, 0, '{pref} {value}'.format(pref='->' if i == option else '  ', value=op))
        op_win.refresh()

        key = stdscr.getkey()
        if key == 'KEY_UP':
            option = max(0, option - 1)
        elif key == 'KEY_DOWN':
            option = min(len(options) - 1, option + 1)
        elif key == '\n':
            break

    return option


def show_question(stdscr, question, answer, options) -> int:
    stdscr.clear()
    curses.cbreak()
    y, x = stdscr.getmaxyx()
    MARGIN = floor(y / 20)
    centered_text(stdscr, MARGIN + 1, question)
    stdscr.refresh()
    centered_text(stdscr, y - MARGIN - 2, "Press space to reveal answer")
    stdscr.refresh()

    while True:
        key = stdscr.getkey()
        if key == ' ':
            break

    COLOURS = {
        "Źle": 3,
        "Trudne": 5,
        "Dobrze": 4,
        "Łatwe": 1
    }

    centered_text(stdscr, floor((y - 2 * MARGIN - 4) / 2) + MARGIN, answer)
    windows = evenly_spaced_windows(len(options), y - MARGIN - 3, 2, x)
    for i, (option, window) in enumerate(zip(options, windows)):
        color = curses.color_pair(COLOURS[option])
        centered_text(window, 0, "({}) {}".format(i + 1, option), color)

    stdscr.refresh()
    key = len(options)
    while key >= len(options) or key < 0:
        key = stdscr.getch() - 49

        if key == 64:
            return -1

    curses.nocbreak()
    return key


def study_deck(stdscr, deck, user):
    for card in deck.get_cards_package_for_today(10):
        answer = show_question(stdscr, card.question, card.answer, card.get_possible_answers())
        if answer >= 0:
            card.set_answer(card.get_possible_answers()[answer])
        else:
            break
        user.save()


def deck_edit_screen(stdscr, wizard: DeckCreationWizard):
    index = 0
    field = 0
    y, x = stdscr.getmaxyx()
    per_page = y - 6
    pages = ceil(len(wizard.cards) / per_page)
    page = 0
    stdscr.clear()

    content_win = curses.newwin(per_page, x-2, 3, 1)
    stdscr.refresh()
    content_win.refresh()

    while True:
        centered_text(stdscr, 1, wizard.name, curses.color_pair(1))
        centered_text(stdscr, y - 2, 'To add new press \'n\'. To edit, highlight and press ENTER, d to delete', curses.color_pair(2))
        centered_text(stdscr, y - 1, 'PAGE-UP, PAGE-DOWN to change pages. \'q\' to exit', curses.color_pair(2))
        content_win.clear()
        content = wizard.cards[(per_page * page):((page + 1) * per_page)]
        for i, card in enumerate(content):
            if i == index:
                content_win.addstr(i, 0, '{}) {} -> {} <<--'.format(card.dc_id+1, card.question, card.answer),
                                   curses.color_pair(2))
            else:
                content_win.addstr(i, 0, '{}) {} -> {}'.format(card.dc_id+1, card.question, card.answer))

        content_win.refresh()
        key = stdscr.getkey()
        if key == 'q' or key == 'Q':
            break
        elif key == 'KEY_DOWN':
            index = min(index + 1, len(content)-1)
        elif key == 'KEY_UP':
            index = max(0, index - 1)
        elif key == '\n':
            edit_card(stdscr, content[index])
            wizard.save()
        elif key == 'KEY_NPAGE':
            page = min(pages-1, page + 1)
        elif key == 'KEY_PPAGE':
            page = max(page - 1, 0)
        elif key == 'n' or key == 'N':
            edit_card(stdscr, wizard.new_card())
            wizard.save()
            pages = ceil(len(wizard.cards) / per_page)
            page = pages - 1
            index = 0
        elif key == 'd' or key == 'D':
            wizard.delete_card(index)
    wizard.save()
