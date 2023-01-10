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
        self.err_string = ""

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
                self.token = ["$", "$"] if self.token[0] == "$" else [
                    None, None]

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
                self.err_string += f'#{self.scanner.line_index + 1} : syntax error , illegal {self.token[1]}\n'

                # a) Skip the current input symbol
                token, string = self.scanner.get_next_token()
                if token == "$":
                    self.err_string += f'#{self.scanner.line_index} : syntax error , Unexpected EOF\n'
                    self.write_files()
                    return
                self.token = [token, string]
                self.token[0] = string if token in [
                    "KEYWORD", "SYMBOL"] else token

                # a) Remove until you reach a goto
                while(not any(value.startswith("goto")
                              for value in list(self.parse_table[self.stack_state[-1]].values()))):
                    self.err_string += f'syntax error , discarded {self.discard_token(self.stack_token[-1])} from stack\n'
                    self.stack_state.pop()
                    self.stack_token.pop()

                discard = True
                while discard:
                    list_of_gotos = []
                    for key, value in self.parse_table[self.stack_state[-1]].items():
                        if "goto" in value and key in self.non_terminals:
                            list_of_gotos.append((key, value))
                    list_of_gotos = sorted(
                        list_of_gotos, key=lambda x: x[0])

                    # c) Stack the nonterminal and goto
                    for rule_goto in list_of_gotos:
                        (non_terminal, state) = rule_goto
                        if self.token[0] in self.follow[non_terminal]:
                            discard = False
                            self.err_string += f'#{self.scanner.line_index + 1} : syntax error , missing {non_terminal}\n'
                            self.stack_token.append([non_terminal, None])
                            action = self.parse_table[self.stack_state[-1]
                                                      ][non_terminal]
                            self.stack_state.append(action.split("_")[1])
                            break

                    # b) Discard zero or more input symbols
                    if discard:
                        self.err_string += f'#{self.scanner.line_index + 1} : syntax error , discarded {self.token[1]} from input\n'
                        token, string = self.scanner.get_next_token()
                        if token == "$":
                            self.err_string += f'#{self.scanner.line_index + 1} : syntax error , Unexpected EOF\n'
                            self.write_files()
                            return
                        self.token = [token, string]
                        self.token[0] = string if token in [
                            "KEYWORD", "SYMBOL"] else token
        self.write_files()

    def discard_token(self, token):
        if token[1] is None:
            return token[0]
        if token[1] in self.scanner.KEYWORD:
            return f"(KEYWORD, {token[1]})"
        elif token[1] in (self.scanner.SYMBOL + self.scanner.EXTRA + ["=="]):
            return f"(SYMBOL, {token[1]})"
        return f"({token[0]}, {token[1]})"

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
            else:
                f.write(self.err_string)
            f.close()
