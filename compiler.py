from scanner import Scanner
from lrparser import Parser

""" Hamila Mailee       97106295 """
""" Sepehr Ilami        97101286 """

scanner = Scanner("input.txt")
parser = Parser(scanner, r"grammar/table.json")
parser.parse()
# tstring = ""
# while (tstring != "$"):
#     ttype, tstring = scanner.get_next_token()
#     print(ttype, ",", tstring)
