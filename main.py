import json
import curses
import levenshtein
import pprint

ENTER_KEYCODE = 10
ESCAPE_KEYCODE = 27
CTRL_C_KEYCODE = 3
BACKSPACE_KEYCODE = 8
LEFT_ARROW_KEYCODE = -2
RIGHT_ARROW_KEYCODE = -2

with open("codon_data.json") as f:
    codon_data = json.load(f)


search_space = []

amino_acid_by_encoding = {}
amino_acid_by_abbreviation = {}
amino_acid_by_letter = {}

lookup_tables = [amino_acid_by_letter, amino_acid_by_abbreviation, amino_acid_by_encoding]

for amino_acid in codon_data:
    search_space.append(amino_acid.lower())
    for acid_info in codon_data[amino_acid]:
        data_entry = codon_data[amino_acid][acid_info]
        if acid_info == 'codes':
            for info in data_entry:
                search_space.append(info.lower())
                amino_acid_by_encoding[info.lower()] = amino_acid
        else:
            search_space.append(data_entry.lower())
            key = data_entry.lower()
            if acid_info == 'abbreviation':
                amino_acid_by_abbreviation[key] = amino_acid
            elif acid_info == 'letter':
                amino_acid_by_letter[key] = amino_acid


print(str(len(search_space))+" "+str( search_space))
pprint.pprint(lookup_tables)
def find_result_by_entry(character):
    if character in codon_data:
        return character, codon_data[character]
    for table in lookup_tables:
        if character in table:
            return table[character], codon_data[table[character]]


def start_search(screen, sIn):
    num_results = 0
    screen_height, screen_width = screen.getmaxyx()
    screen.addstr(1, 1, "Search: %s"%sIn)
    search_results = []
    if len(sIn) == 0:
        return
    for v in search_space:
        distance = levenshtein.iterative_levenshtein(sIn.lower(), v.lower())
        search_results.append((distance, v))
        num_results+=1

    search_results.sort()

    draw_line = 2
    for result in search_results:
        if draw_line < screen_height - 1:
            lookup_result = find_result_by_entry(result[1])
            if lookup_result is None:
                continue
            amino_acid, acid_info = lookup_result

            screen.addstr(draw_line, 1, str(result[1])+" "+str(result[0])+" "+": "+amino_acid)
            draw_line+=1

            for acid_info_entry in acid_info:
                if draw_line < screen_height-1:
                    screen.addstr(draw_line, 4, acid_info_entry+": "+str(acid_info[acid_info_entry]))
                    draw_line+=1

        else:
            break

def main(stdscr):
    curses.curs_set(False)
    curses.cbreak()
    stdscr.nodelay(1)

    running = True

    legal_chars = set("abcdefghijklmnopqrstuvwxyz ")

    screen_height, screen_width = stdscr.getmaxyx()

    search_bar = curses.newpad(3, screen_width-2)
    search_bar.keypad(True)

    result_space = curses.newwin(screen_height -5, screen_width-2, 4, 1)

    typed_string = []
    cursor_pos = 0

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
                typed_string.insert(cursor_pos, chr(char))
                start_search(result_space, ''.join(typed_string))
                cursor_pos+=1

            elif keycode_in == ENTER_KEYCODE:
                start_search(result_space, ''.join(typed_string))
                typed_string = []
                cursor_pos = 0
            elif keycode_in == CTRL_C_KEYCODE or keycode_in == ESCAPE_KEYCODE:
                running = False
            elif keycode_in == BACKSPACE_KEYCODE:
                if cursor_pos > 0:
                    typed_string = typed_string[:cursor_pos-1] + typed_string[cursor_pos:]
                    start_search(result_space, ''.join(typed_string))
                    cursor_pos = max(cursor_pos-1, 0)
            elif keycode_in == curses.KEY_DC:
                if cursor_pos < len(typed_string):
                    typed_string = typed_string[:cursor_pos] + typed_string[cursor_pos+1:]
                    start_search(result_space, ''.join(typed_string))

            elif keycode_in == curses.KEY_LEFT:
                cursor_pos = max(cursor_pos-1, 0)
            elif keycode_in == curses.KEY_RIGHT:
                cursor_pos = min(cursor_pos+1, len(typed_string))

        string_out = ''.join(typed_string)
        search_bar.addstr(1, 1, string_out[:cursor_pos]+"_"+string_out[cursor_pos:])



        stdscr.refresh()
        search_bar.refresh(0, 0, 1, 1, 3, screen_width - 2)
        result_space.refresh()

curses.wrapper(main)
