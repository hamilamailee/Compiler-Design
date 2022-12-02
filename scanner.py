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

        self.lines = open(input_file).readlines()
        self.start = 0
        self.pointer = 0
        self.state = 0

    def tokenize(self):
        line_index = 0
        for line in self.lines:
            self.get_next_token(line.strip(), line_index)
            line_index += 1

    def get_next_token(self, line, line_index):
        tokens = []
        errors = []
        while self.pointer != len(line):
            char = line[self.pointer]
            # print("chars is:{} in pointer:{}. State:{}".format(
            #     char, self.pointer, self.state))
            if self.state == 0:
                if char in self.SYMBOL:
                    tokens.append("(SYMBOL, {})".format(char))
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
                    pass
                else:
                    errors.append("({}, Invalid input)".format(char))
            elif self.state == 1:
                if char in self.LETTER or char in self.DIGIT:
                    pass
                elif char in (self.WHITESPACE + self.SYMBOL + self.EXTRA):
                    if line[self.start:self.pointer] in self.KEYWORD:
                        tokens.append("(KEYWORD, {})".format(
                            line[self.start:self.pointer]))
                    else:
                        tokens.append("(ID, {})".format(
                            line[self.start:self.pointer]))
                    self.state = 0
                    continue
                else:
                    errors.append("({}, Invalid input)".format(
                        line[self.start:self.pointer+1]))
                    self.state = 0
            elif self.state == 3:
                if char in self.DIGIT:
                    pass
                elif char not in self.LETTER:
                    tokens.append("(NUM, {})".format(
                        line[self.start:self.pointer]))
                    self.state = 0
                    continue
                else:
                    errors.append("({}, Invalid number)".format(
                        line[self.start:self.pointer+1]))
                    self.state = 0
            elif self.state == 6:
                self.state = 0
                if char == "=":
                    tokens.append("(SYMBOL, ==)")
                else:
                    tokens.append("(SYMBOL, =)")
                    continue
            elif self.state == 8:
                self.state = 0
                if char == "/":
                    errors.append("(*/, Unmatched comment)")
                else:
                    tokens.append("(SYMBOL, *)")
                    continue
            elif self.state == 10:
                if char == "/":
                    self.state = 11
                    self.start = self.pointer - 1
                elif char == "*":
                    self.state = 13
                    self.start = self.pointer - 1
                else:
                    tokens.append("(SYMBOL, /)")
                    self.state = 0
                    continue
            elif self.state == 11:
                if self.pointer != len(line) - 1:
                    pass
                else:
                    # tokens.append("(COMMENT,{})".format(
                    #     line[self.start:self.pointer+1]))
                    self.state = 0
            self.pointer += 1
        if len(tokens) > 0:
            print("\nTOKENS:")
            for t in tokens:
                print(t, end=" ")
            print("\nERRORS:")
            for e in errors:
                print(e, end=" ")
        self.pointer = 0
        return None
