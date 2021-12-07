import sys
from enum import Enum

class TokenType(Enum):
    CHAR_NEWLINE = 0
    EOF = 1
    BINOP_PLUS = 2
    BINOP_MINUS = 3
    BINOP_MUL = 4
    BINOP_DIV = 5
    LITERAL_NUMBER = 6
    LITERAL_STRING = 7

class Token:
    def __init__(self, tk, rep):
        self.type = tk
        self.repr = rep

class Lexer:
    def __init__(self, source, file_name):
        self.source = source.strip()
        self.file_name = file_name
        self.current_index = 0
        self.current_line = 1
        self.current_char = self.source[self.current_index]

    def error_and_die(self, message):
        print(f"File: \"<{self.file_name}>\"")
        print(f"[ERROR]: {message} \n    at line: {self.current_line}")
        sys.exit(1)

    def advance(self):
        self.current_index += 1

        if self.current_index >= len(self.source):
            self.current_char = '\0'
        elif self.current_char == '\n':
            self.current_line += 1
            self.current_char = self.source[self.current_index]
        else:
            self.current_char = self.source[self.current_index]

    def skip_whitespaces(self):
        while self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\r':
            self.advance()

    def skip_comments(self):
        if self.current_char == '#':
            while self.current_char != '\n' and self.current_char != '\0':
                self.advance()

    def get_token(self):
        self.skip_whitespaces()
        self.skip_comments()

        token = None

        if self.current_char == '\0':
            token = Token(TokenType.EOF, None)
        elif self.current_char == '\n':
            token = Token(TokenType.CHAR_NEWLINE, None)
        elif self.current_char == '+':
            token = Token(TokenType.BINOP_PLUS, self.current_char)
        elif self.current_char == '-':
            token = Token(TokenType.BINOP_MINUS, self.current_char)
        elif self.current_char == '*':
            token = Token(TokenType.BINOP_MUL, self.current_char)
        elif self.current_char == '/':
            token = Token(TokenType.BINOP_DIV, self.current_char)
        elif self.current_char == '"':
            start_pos = self.current_index
            string = ''
            self.advance()

            while self.current_char != '"' and self.current_char != '\0' and self.current_char != '\n':
                string += self.current_char
                self.advance()

            end_pos = self.current_index

            if self.current_char == '\0' or self.current_char == '\n':
                self.error_and_die(f"( {self.source[start_pos:end_pos:]} ) \nmissing double quotes after opening quotes")

            token = Token(TokenType.LITERAL_STRING, string)
        elif self.current_char >= '0' and self.current_char <= '9':
            decimal_count = 0
            num_str = ''
            num_str += self.current_char
            self.advance()

            while (self.current_char >= '0' and self.current_char <= '9') or self.current_char == '.':
                if self.current_char == '.':
                    decimal_count += 1
                    if decimal_count >= 2:
                        self.error_and_die(f"unexpected token \"{self.current_char}\" before {num_str}")

                num_str += self.current_char
                self.advance()

            if num_str.endswith('.'):
                num_str += '0'

            token = Token(TokenType.LITERAL_NUMBER, num_str)
        else:
            self.error_and_die(f"unexpected token \"{self.current_char}\"")

        self.advance()

        return token