from scanner import Scanner
from lrparser import Parser
import os

files = ["parse_tree.txt", "syntax_errors.txt"]


def find_dif_files(file1, file2):
    print("{} vs {}".format(file1, file2))
    # reading files
    f1 = open(file1, "r", encoding="utf-8")
    f2 = open(file2, "r", encoding="utf-8")

    i = 0

    for line1 in f1:
        i += 1

        for line2 in f2:

            # matching line1 from both files
            if line1 == line2:
                # print IDENTICAL if similar
                pass
                # print("Line ", i, ": IDENTICAL")
            else:
                print("Line ", i, ":")
                # else print that line from both files
                print("\t{}:".format(file1), line1, end='')
                print("\t{}:".format(file2), line2, end='')
            break

    # closing files
    f1.close()
    f2.close()


def initialize_files():
    for f in files:
        if os.path.exists(f):
            os.remove(f)


testcases = "Testcases-P2"

for i in os.listdir(testcases):
    print("TEST NUMBER", i)
    initialize_files()

    scanner = Scanner(os.path.join(testcases, i, "input.txt"))
    parser = Parser(scanner, r"grammar/table.json")
    parser.parse()

    for f in files:
        find_dif_files(os.path.join(testcases, i, f), f)

    print("==================================================")
