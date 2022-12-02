from scanner import Scanner
import os
from difflib import Differ

tok = "tokens.txt"
sym = "symbol_table.txt"
lex = "lexical_errors.txt"


def find_dif_files(file1, file2):
    with open(file1) as file_1, open(file2) as file_2:
        differ = Differ()

    for line in differ.compare(file_1.readlines(), file_2.readlines()):
        print(line)


def initialize_files():
    if os.path.exists(tok):
        os.remove(tok)
    if os.path.exists(sym):
        os.remove(sym)
    if os.path.exists(lex):
        os.remove(lex)


testcases = "Testcases"

for i in os.listdir(testcases):
    initialize_files()
    scanner = Scanner(os.path.join(testcases, i, "input.txt"))
    scanner.tokenize()

    try:
        find_dif_files(os.path.join(testcases, i, tok), tok)
        find_dif_files(os.path.join(testcases, i, sym), sym)
        find_dif_files(os.path.join(testcases, i, lex), lex)
    except:
        print("Testcases with no output.")
