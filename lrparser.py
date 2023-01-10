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

        self.root = None
        self.nodes = []

        self.error = False

    def parse(self):
        while (self.action != "accept"):

            if self.token is None:
                token, string = self.scanner.get_next_token()
                self.token = string if token in [
                    "KEYWORD", "SYMBOL"] else token

            try:
                self.action = self.parse_table[self.stack_state[-1]][self.token]
            except:
                self.action = "PANIC"

            if self.action == ("accept"):
                continue

            elif self.action.startswith("shift"):
                self.update_stack(self.token, Node(
                    "({}, {})".format(token, string)))
                self.token = "$" if self.token == "$" else None

            elif self.action.startswith("reduce"):
                production_rule = self.grammar[self.action.split("_")[1]]

                self.root = Node(production_rule[0])
                if self.root.name == "program":
                    end = Node("$", parent=self.root)

                if production_rule[-1] != 'epsilon':
                    self.stack_token = self.stack_token[:2 -
                                                        len(production_rule)]
                    self.stack_state = self.stack_state[: 2 -
                                                        len(production_rule)]
                    for i in range(len(production_rule) - 2):
                        top = self.nodes.pop()[1]
                        top.parent = self.root
                else:
                    top = Node("epsilon")
                    top.parent = self.root

                self.action = self.parse_table[self.stack_state[-1]
                                               ][production_rule[0]]
                self.update_stack(production_rule[0], self.root)

            else:
                self.error = True
                # TODO: PANIC MODE IMPLEMENTATION
                print(f'#line_number : syntax error , illegal {self.token}')
                self.stack_state.pop()
                self.stack_state.pop()
                while("goto" not in value for value in self.parse_table[self.stack_state[-1]].values()):
                    self.stack_state.pop()
                    self.stack_state.pop()
                error_handling = self.parse_table[self.stack_state[-1]
                                                  ][self.stack_state[-2]]
                ac, ind = error_handling.split("_")
                list_of_gotos = []
                for (key, value) in self.parse_table[self.stack_state[-1]]:
                    if "goto" in value:
                        list_of_gotos.append((key, value))
                list_of_gotos = sorted(list_of_gotos, key=lambda x: x[1])
                try:
                    input, string = self.scanner.get_next_token()
                    if input in ["KEYWORD", "SYMBOL"]:
                        input = string
                except:
                    input = "$"
                for i in range(len(list_of_gotos)):
                    key, value = list_of_gotos[i]
                    if input in self.follow[key]:
                        # add key to the stack
                        self.stack_state.append(key)
                        ac = self.parse_table[self.stack_state[-2]
                                              ][self.stack_state[-1]]
                        number = ac.split("_")[1]
                        self.stack_state.append(number)
                        break
                return

        self.write_files()

    def update_stack(self, token, node: Node):
        if self.action == "accept":
            return
        self.stack_token.append(token)
        self.stack_state.append(self.action.split("_")[1])
        self.nodes.append([node.name, node])

    def write_files(self):
        with open('parse_tree.txt', 'a',  encoding='utf-8') as f:
            for pre, fill, node in RenderTree(self.root, childiter=reversed):
                f.write("%s%s\n" % (pre, node.name))
            f.close()

        with open('syntax_errors.txt', 'a', encoding='utf-8') as f:
            if not self.error:
                f.write("There is no syntax error.")
            f.close()
