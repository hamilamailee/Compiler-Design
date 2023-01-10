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
        self.token = [None, None]
        self.action = "shift"

        self.root = None
        self.nodes = []

        self.error = False

    def parse(self):
        while (self.action != "accept"):

            if self.token[0] is None:
                token, string = self.scanner.get_next_token()
                self.token = [token, string]
                self.token[0] = string if token in [
                    "KEYWORD", "SYMBOL"] else token

            try:
                self.action = self.parse_table[self.stack_state[-1]
                                               ][self.token[0]]
            except:
                self.action = "PANIC"

            if self.action == ("accept"):
                continue

            elif self.action.startswith("shift"):
                self.update_stack(self.token, Node(
                    "({}, {})".format(token, string)))
                self.token[0] = "$" if self.token[0] == "$" else None

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
                self.update_stack([production_rule[0], None], self.root)

            else:
                self.error = True
                # TODO: PANIC MODE IMPLEMENTATION
                print(
                    f'#{self.scanner.line_index + 1} : syntax error , illegal {self.token[0]}')
                token, string = self.scanner.get_next_token()
                self.token = [token, string]
                self.token[0] = string if token in [
                    "KEYWORD", "SYMBOL"] else token

                while(not any(value.startswith("goto") for value in list(self.parse_table[self.stack_state[-1]].values()))):
                    print(
                        list(self.parse_table[self.stack_state[-1]].values()))
                    print(
                        f'syntax error , discarded ({self.get_tok(self.token)}, {self.token[1]}) from stack')
                    self.stack_state.pop()
                    self.stack_token.pop()
                while True:
                    try:
                        error_handling = self.parse_table[self.stack_state[-1]
                                                          ][self.token[0]]
                        break
                    except:
                        print(
                            f'#{self.scanner.line_index + 1} : syntax error , discarded {self.token[0]} from input')
                        token, string = self.scanner.get_next_token()
                        self.token = string if token in [
                            "KEYWORD", "SYMBOL"] else token

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

    def get_tok(self, token):
        if token[1] in self.scanner.KEYWORD:
            return "KEYWORD"
        elif token[1] in (self.scanner.SYMBOL + self.scanner.EXTRA + ["=="]):
            return "SYMBOL"
        return token[0]

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
