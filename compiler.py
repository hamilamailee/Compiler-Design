from scanner import Scanner
import os

""" Hamila Mailee       97106295 """
""" Sepehr Ilami        """
""" 
    References:
        [1]
"""

testcases = "Testcases"

for i in os.listdir(testcases):
    scanner = Scanner(os.path.join(testcases, i, "input.txt"))
    scanner.tokenize()
    break

print("salam"[1:2])
