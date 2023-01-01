class Scanner:
    def __init__(self, input_file) -> None:

        self.LETTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.DIGIT = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.KEYWORD = ["if", "else", "void", "int", "while", "break",
                        "switch", "default", "case", "return", "endif"]
        self.SYMBOL = [";", ":", ",", "[", "]",
                       "(", ")", "{", "}", "+", "-", "<"]
        self.WHITESPACE = [" ", "\n", "\r", "\t", "\v", "\f"]
        self.EXTRA = ["=", "*", "/"]
        self.VALID = (self.DIGIT + self.KEYWORD +
                      self.SYMBOL + self.WHITESPACE + self.EXTRA)

        self.lines = open(input_file).readlines()
        self.symbols = set(self.KEYWORD)
        self.line_index = 0
        self.start = 0
        self.pointer = 0
        self.state = 0
        self.errors = 0
        self.comment_line = 0

    def get_next_token(self):
        line = self.lines[self.line_index].strip()
        line = line + "\n"

        while self.pointer != len(line) and self.line_index <= len(self.lines) - 1:
            char = line[self.pointer]

            #   STARTING FROM STATE0   #
            if self.state == 0:
                if char in self.SYMBOL:
                    self.pointer += 1
                    return "SYMBOL", char
                elif char in self.LETTER:
                    self.state = 1
                    self.start = self.pointer
                elif char in self.DIGIT:
                    self.state = 3
                    self.start = self.pointer
                elif char == "=":
                    self.state = 6
                elif char == "*":
                    self.state = 8
                elif char == "/":
                    self.state = 10
                elif char in self.WHITESPACE:
                    if char == "\n":
                        line = self.next_line()
                        continue
                    pass
                else:
                    self.pointer += 1
                    return char, "Invalid input"

            #   STARTING FROM STATE1   #
            elif self.state == 1:
                if char in self.LETTER or char in self.DIGIT:
                    pass
                elif char in (self.WHITESPACE + self.SYMBOL + self.EXTRA):
                    if line[self.start:self.pointer] in self.KEYWORD:
                        self.state = 0
                        return "KEYWORD", line[self.start:self.pointer]
                    else:
                        self.state = 0
                        return "ID", line[self.start:self.pointer]
                else:
                    self.state = 0
                    self.pointer += 1
                    return line[self.start:self.pointer], "Invalid input"

            #   STARTING FROM STATE3   #
            elif self.state == 3:
                if char in self.DIGIT:
                    pass
                elif char not in self.LETTER:
                    self.state = 0
                    return "NUM", line[self.start:self.pointer]
                else:
                    self.state = 0
                    self.pointer += 1
                    return line[self.start:self.pointer], "Invalid number"

            #   STARTING FROM STATE6   #
            elif self.state == 6:
                self.state = 0
                if char == "=":
                    self.pointer += 1
                    return "SYMBOL", "=="
                elif char not in self.VALID:
                    self.pointer += 1
                    return line[self.pointer-2:self.pointer], "Invalid input"
                else:
                    return "SYMBOL", "="

            #   STARTING FROM STATE8   #
            elif self.state == 8:
                self.state = 0
                if char == "/":
                    self.pointer += 1
                    return "*/", "Unmatched comment"
                else:
                    return "SYMBOL", "*"

            #   STARTING FROM STATE10  #
            elif self.state == 10:
                if char == "/":
                    self.state = 11
                    self.start = self.pointer - 1
                elif char == "*":
                    self.state = 13
                    self.start = self.pointer - 1
                    self.comment_line = self.line_index
                else:
                    self.state = 0
                    return "SYMBOL", "/"

            #   STARTING FROM STATE11  #
            elif self.state == 11:
                if char != "\n":
                    pass
                else:
                    self.state = 0
                    line = self.next_line()
                    continue

            #   STARTING FROM STATE13  #
            elif self.state == 13:
                if char == "*":
                    self.state = 14
                elif char == "\n":
                    line = self.next_line()
                    continue

            #   STARTING FROM STATE14  #
            elif self.state == 14:
                if char == "/":
                    self.state = 0
                elif char != "*":
                    self.state = 13
                elif char == "\n":
                    line = self.next_line()
                    continue

            self.pointer += 1

        return "$", "$"

    def next_line(self):
        self.pointer = 0
        self.line_index += 1
        try:
            return self.lines[self.line_index].strip() + "\n"
        except:
            return "$"
