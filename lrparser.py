import json
from anytree import Node, RenderTree
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

        self.error = False

    def parse(self):
        while (self.action != "accept"):
            if self.token is None:
                try:
                    self.token, string = self.scanner.get_next_token()
                    self.strings.append("({}, {})".format(self.token, string))
                    if self.token in ["KEYWORD", "SYMBOL"]:
                        self.token = string
                except:
                    self.token = "$"
            action = self.parse_table[self.stack_state[-1]][self.token]
            if action == "accept":
                self.action = action
                continue
            self.action, index = action.split("_")
            if self.action == "shift":
                self.stack_token.append(self.token)
                self.stack_state.append(index)
                self.token = None
            elif self.action == "reduce":
                production_rule = self.grammar[index]
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
            else:
                self.error = True

        self.write_files()

    def generate_parse_tree(self, root_node, root_children):
        children = dict()
        for c in root_children[2:]:
            children[c] = Node(c, parent=root_node)

        for c in list(children)[::-1]:
            if len(self.reductions) == 0:
                return
            if self.reductions[-1][0] == c:
                self.generate_parse_tree(children[c], self.reductions.pop())
                children.pop(c)

    def write_files(self):
        root = Node(self.reductions[-1][0])
        self.generate_parse_tree(root, self.reductions.pop())
        end = Node("$", parent=root)

        self.strings.pop()
        for l in root.leaves[::-1][1:]:
            if l.name != "epsilon":
                l.name = self.strings.pop()

        with open('parse_tree.txt', 'a',  encoding='utf-8') as f:
            for pre, fill, node in RenderTree(root):
                f.write("%s%s\n" % (pre, node.name))
            f.close()

        with open('syntax_erros.txt', 'a', encoding='utf-8') as f:
            if not self.error:
                f.write("There is no syntax error.")
            f.close()
