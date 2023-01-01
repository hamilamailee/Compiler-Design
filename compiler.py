from scanner import Scanner

""" Hamila Mailee       97106295 """
""" Sepehr Ilami        97101286 """

scanner = Scanner("input.txt")
tstring = "start"
while (tstring != "$"):
    ttype, tstring = scanner.get_next_token()
    print(ttype, ",", tstring)
