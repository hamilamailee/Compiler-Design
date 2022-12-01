class Scanner:
    def __init__(self, input_file) -> None:

        self.LETTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.DIGIT = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.KEYWORD = ["if", "else", "void", "int", "while", "break",
                        "switch", "default", "case", "return", "endif"]
        self.SYMBOL = [";", ":", ",", "[", "]",
                       "(", ")", "{", "}", "+", "-", "*", "=", "<", "/"]
        self.WHITESPACE = [" ", "\n", "\r", "\t", "\v", "\f"]

        self.lines = open(input_file).readlines()
        self.start = 0
        self.pointer = 0
        self.state = 0

    def tokenize(self):
        for line in self.lines:
            self.get_next_token(line.strip())

    def get_next_token(self, line):
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
                    self.start = self.pointer
                elif char == "*":
                    self.state = 8
                    self.start = self.pointer
                elif char == "/":
                    self.state = 10
                    self.start = self.pointer
                elif char in self.WHITESPACE:
                    pass
            elif self.state == 1:
                if char in self.LETTER or char in self.DIGIT:
                    pass
                else:
                    if line[self.start:self.pointer] in self.KEYWORD:
                        tokens.append("(KEYWORD, {})".format(
                            line[self.start:self.pointer]))
                    else:
                        tokens.append("(ID, {})".format(
                            line[self.start:self.pointer]))
                    self.state = 0
                    continue
            elif self.state == 3:
                if char in self.DIGIT:
                    pass
                elif char not in self.LETTER:
                    tokens.append("(NUM, {})".format(
                        line[self.start:self.pointer]))
                    self.state = 0
                    continue
                else:
                    errors.append("({}, Invaid number)".format(
                        line[self.start:self.pointer+1]))
                    self.state = 0
            self.pointer += 1
        print("\nTOKENS:")
        for t in tokens:
            print(t, end=" ")
        print("\nERRORS:")
        for e in errors:
            print(e, end="")
        self.pointer = 0
        return None
