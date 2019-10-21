# search bar that handles the backend for typing into a text box

class TextBox:
    def __init__(self, cursor = '_'):
        self.cursor_pos = 0
        self.typed_string = []
        self.cursor = cursor

    def insert_letter(self, letter):
        self.typed_string.insert(self.cursor_pos, letter)
        self.cursor_pos += 1

    def clear_searchbar(self):
        self.typed_string = []
        self.cursor_pos = 0

    def backspace(self):
        if self.cursor_pos > 0:
            self.typed_string = self.typed_string[:self.cursor_pos - 1] + self.typed_string[self.cursor_pos:]
            self.cursor_pos = max(self.cursor_pos - 1, 0)

    def delete(self):
        if self.cursor_pos < len(self.typed_string):
            self.typed_string = self.typed_string[:self.cursor_pos] + self.typed_string[self.cursor_pos + 1:]

    def cursor_left(self):
        self.cursor_pos = max(self.cursor_pos - 1, 0)

    def cursor_right(self):
        self.cursor_pos = min(self.cursor_pos + 1, len(self.typed_string))

    def home(self):
        self.cursor_pos = 0

    def end(self):
        self.cursor_pos = len(self.typed_string)

    def get_string(self):
        return ''.join(self.typed_string)

    def get_string_with_cursor(self):
        string_out = self.get_string()
        return string_out[:self.cursor_pos] + self.cursor + string_out[self.cursor_pos:]
