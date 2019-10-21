import amino_acid_dictionary
import curses, textbox

ENTER_KEYCODE = 10
ESCAPE_KEYCODE = 27
CTRL_C_KEYCODE = 3
BACKSPACE_KEYCODE = 8
LEFT_ARROW_KEYCODE = -2
RIGHT_ARROW_KEYCODE = -2

amino_acids = amino_acid_dictionary.AAcidDictionary("codon_data.json")


def start_search(screen, sIn):
    screen_height, screen_width = screen.getmaxyx()
    screen.addstr(1, 1, "Search: %s" % sIn)
    if len(sIn) == 0:
        return

    # list of (amino acid; string, info about the amino acid; dict of (attribute:info ))
    search_results = amino_acids.query(sIn)

    draw_line = 2
    for result in search_results:
        if draw_line < screen_height - 1:
            for lookup_result in result[1]:
                amino_acid, acid_info = lookup_result
                if draw_line < screen_height - 1:
                    screen.addstr(draw_line, 1, result[0] + ": " + amino_acid, curses.color_pair(1))
                    draw_line += 1

                    for acid_info_entry in acid_info:
                        if draw_line < screen_height - 1:
                            screen.addstr(draw_line, 4, acid_info_entry + ": " + str(acid_info[acid_info_entry]))
                            draw_line += 1

        else:
            break


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(False)
    curses.cbreak()

    running = True

    legal_chars = set("abcdefghijklmnopqrstuvwxyz ")

    screen_height, screen_width = stdscr.getmaxyx()

    search_bar = curses.newpad(3, screen_width - 2)
    search_bar.keypad(True)

    result_space = curses.newwin(screen_height - 5, screen_width - 2, 4, 1)

    search_bar_text_box = textbox.TextBox()

    splash_text = ("Made by Aaron Li 2019",
                   "Enter to start")
    for i, v in enumerate(splash_text):
        stdscr.addstr(screen_height // 2 - 2 + i, screen_width // 2 - len(v) // 2, v)
    stdscr.refresh()

    while running:
        search_bar_height, search_bar_width = search_bar.getmaxyx()
        search_bar.clear()
        stdscr.clear()
        result_space.clear()

        stdscr.border()
        search_bar.border()
        result_space.border()

        char = search_bar.getch()

        if char is not None:
            keycode_in = char

            if chr(char).lower() in legal_chars:
                search_bar_text_box.insert_letter(chr(char))
                start_search(result_space, search_bar_text_box.get_string())

            elif keycode_in == ENTER_KEYCODE:
                start_search(result_space, search_bar_text_box.get_string())
                search_bar_text_box.clear_searchbar()

            elif keycode_in == CTRL_C_KEYCODE or keycode_in == ESCAPE_KEYCODE:
                running = False
            elif keycode_in == BACKSPACE_KEYCODE:
                search_bar_text_box.backspace()
                start_search(result_space, search_bar_text_box.get_string())
            elif keycode_in == curses.KEY_DC:
                search_bar_text_box.delete()
                start_search(result_space, search_bar_text_box.get_string())

            elif keycode_in == curses.KEY_LEFT:
                search_bar_text_box.cursor_left()
                start_search(result_space, search_bar_text_box.get_string())
            elif keycode_in == curses.KEY_RIGHT:
                search_bar_text_box.cursor_right()
                start_search(result_space, search_bar_text_box.get_string())
            elif keycode_in == curses.KEY_RESIZE:
                curses.curs_set(False)
                screen_height, screen_width = stdscr.getmaxyx()

                search_bar.resize(3, screen_width - 2)

                result_space.resize(screen_height - 5, screen_width - 2)

                search_bar.clear()
                stdscr.clear()
                result_space.clear()

                stdscr.border()
                search_bar.border()
                result_space.border()

                start_search(result_space, search_bar_text_box.get_string())
            elif keycode_in == curses.KEY_HOME:
                search_bar_text_box.home()
                start_search(result_space, search_bar_text_box.get_string())

            elif keycode_in == curses.KEY_END:
                search_bar_text_box.end()
                start_search(result_space, search_bar_text_box.get_string())

        search_bar.addstr(1, 1, search_bar_text_box.get_string_with_cursor())

        stdscr.refresh()
        search_bar.refresh(0, 0, 1, 1, 3, screen_width - 2)
        result_space.refresh()


curses.wrapper(main)
