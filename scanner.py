class Scanner:
    def __init__(self, input_file) -> None:

        self.LETTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.DIGIT = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.KEYWORD = ["if", "else", "void", "int", "while", "break",
                        "switch", "default", "case", "return", "endif"]
        self.SYMBOL = [";", ":", ",", "[", "]",
                       "(", ")", "{", "}", "+", "-", "*", "=", "<", "==", "/"]
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
        while self.pointer != len(line):
            char = line[self.pointer]
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
                    continue
            self.pointer += 1
        for t in tokens:
            print(t, end=" ")
        self.pointer = 0
        return None
