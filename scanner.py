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
        self.symbols = set()
        self.start = 0
        self.pointer = 0
        self.state = 0
        self.errors = 0
        self.comment_line = 0
        self.comment_start = 0

        self.tokens = open("tokens.txt", "a+")
        self.lexical_erros = open("lexical_errors.txt", "a+")
        self.symbol_table = open("symbol_table.txt", "a+")

    def tokenize(self):
        line_index = 0
        for line in self.lines:
            self.errors += self.get_next_token(line.strip(), line_index)
            line_index += 1

        string = ""
        for i in range(len(self.symbols)):
            string += "{}.\t".format(i+1) + self.symbols.pop() + "\n"
        self.symbol_table.write(string)
        self.symbol_table.close()
        self.tokens.close()

        if self.state != 0:
            self.errors += 1
            err_str = self.lines[self.comment_line][self.start:] + \
                "".join(self.lines[self.comment_line+1:])
            if len(err_str) >= 7:
                err_str = err_str[:7]+"..."
            self.lexical_erros.write("{}.\t".format(
                self.comment_line + 1) + "({}, Unclosed comment)".format(err_str))
        if self.errors == 0:
            self.lexical_erros.write("There is no lexical error.")
        self.lexical_erros.close()

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
                        self.symbols.add(line[self.start:self.pointer])
                    else:
                        tokens.append("(ID, {})".format(
                            line[self.start:self.pointer]))
                        self.symbols.add(line[self.start:self.pointer])
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
                    self.comment_start = self.pointer - 1
                    self.comment_line = line_index
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
            elif self.state == 13:
                if char == "*":
                    self.state = 14
            elif self.state == 14:
                if char != "*" or char != "/":
                    self.state = 13
                elif char == "/":
                    self.state = 0
            self.pointer += 1
        # if len(tokens) > 0:
        #     print("\nTOKENS:")
        #     for t in tokens:
        #         print(t, end=" ")
        # if len(errors) > 0:
        #     print("\nERRORS:")
        #     for e in errors:
        #         print(e, end=" ")
        self.pointer = 0
        if len(tokens) > 0:
            string = "{}.\t".format(line_index + 1) + " ".join(tokens) + "\n"
            self.tokens.write(string)
        if len(errors) > 0:
            string = "{}.\t".format(line_index + 1) + " ".join(errors) + "\n"
            self.lexical_erros.write(string)

        return len(errors)
