class Scanner:
    def __init__(self, input_file) -> None:

        self.KEYWORD = ["if", "else", "void", "int", "while", "break",
                        "switch", "default", "case", "return", "endif"]
        self.SYMBOL = [";", ":", ",", "[", "]",
                       "(", ")", "{", "}", "+", "-", "*", "=", "<", "==", "/"]
        self.WHITESPACE = [" ", "\n", "\r", "\t", "\v", "\f"]

        self.lines = open(input_file).readlines()
        self.start = 0
        self.state = 0
        self.counter = 0

    def tokenize(self):
        for line in self.lines:
            self.get_next_token(line.strip())

    def get_next_token(self, line):
        tokens = []
        while self.counter != len(line):
            char = line[self.counter]
            if char in self.SYMBOL:
                tokens.append("(SYMBOL, {})".format(char))
            self.counter += 1
        for t in tokens:
            print(t, end=" ")
        self.counter = 0
        return None
