from scanner import Scanner
import os

tok = "tokens.txt"
sym = "symbol_table.txt"
lex = "lexical_errors.txt"


def find_dif_files(file1, file2):
    print("{} vs {}".format(file1, file2))
    # reading files
    f1 = open(file1, "r")
    f2 = open(file2, "r")

    i = 0

    for line1 in f1:
        i += 1

        for line2 in f2:

            # matching line1 from both files
            if line1 == line2:
                # print IDENTICAL if similar
                print("Line ", i, ": IDENTICAL")
            else:
                print("Line ", i, ":")
                # else print that line from both files
                print("\t{}:\t".format(file1), line1, end='')
                print("\t{}:\t\t\t".format(file2), line2, end='')
            break

    # closing files
    f1.close()
    f2.close()


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
        # find_dif_files(os.path.join(testcases, i, sym), sym)
        find_dif_files(os.path.join(testcases, i, lex), lex)
    except:
        print("Testcases with no output.")
    break
