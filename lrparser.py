import json
from scanner import Scanner


class Parser:

    def __init__(self, scanner: Scanner, grammar_json) -> None:
        self.scanner = scanner
        grammar = json.load(open(grammar_json))
        self.terminals = grammar['terminals']
        self.non_terminals = grammar['non_terminals']
        self.first = grammar['first']
        self.follow = grammar['follow']
        self.grammar = grammar['grammar']
        self.parse_table = grammar['parse_table']

        self.stack_state = ["0"]
        self.stack_token = []
        self.token = None
        self.action = "shift"

        self.reductions = []
        self.strings = []

        # print(self.grammar)
        self.parse()

    def parse(self):
        while (self.action != "accept"):
            print("state stack:\t", self.stack_state)
            print("string stack:\t", self.stack_token)

            if self.token is None:
                try:
                    self.token, string = self.scanner.get_next_token()
                    if self.token in ["KEYWORD", "SYMBOL"]:
                        self.token = string
                except:
                    self.token = "$"
            print("input:\t", self.token)
            action = self.parse_table[self.stack_state[-1]][self.token]
            if action == "accept":
                self.action = action
                continue
            self.action, index = action.split("_")
            print("action:", self.action, "state:", index)
            if self.action == "shift":
                self.stack_token.append(self.token)
                self.stack_state.append(index)
                self.token = None
            elif self.action == "reduce":
                production_rule = self.grammar[index]
                print("Production Rule:\t", production_rule)
                if production_rule[-1] != 'epsilon':
                    self.stack_token = self.stack_token[:2 -
                                                        len(production_rule)]
                    self.stack_state = self.stack_state[:2 -
                                                        len(production_rule)]

                action = self.parse_table[self.stack_state[-1]
                                          ][production_rule[0]]
                self.reductions.append(production_rule)
                if action == "accept":
                    self.action = "accept"
                    continue

                self.action, index = action.split("_")
                self.stack_token.append(production_rule[0])
                self.stack_state.append(index)
                print("action index", index, self.action)
                print("NEW state stack:\t", self.stack_state)
                print("NEW string stack:\t", self.stack_token)
            else:
                break
            print("=====================================================")
        self.generate_parse_tree()

    def generate_parse_tree(self):
        print(self.reductions)
