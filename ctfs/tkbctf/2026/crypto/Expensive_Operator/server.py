import os
import signal
import re
from Crypto.Util.number import getPrime

signal.alarm(150)

flag = os.environ.get("FLAG", "tkbctf{dummy}")
target = getPrime(512)
print(f"{target = }")

cost = 0
variables = {"one": 1}
while True:
    expr = input(">>> ")
    if not re.fullmatch(r"[a-z]+=[a-z]+[+*][a-z]+", expr):
        print("SyntaxError")
        continue
    cost += expr.count("+")
    exec(expr, {"__builtins__": None}, variables)
    if expr.startswith("result="):
        break

if variables["result"] != target:
    print("Wrong answer!")
    exit(1)
score = 2300 // cost
print(f"Score: {score} / 100")
if score >= 100:
    print(f"You passed my exam! flag: {flag}")
else:
    print("Try harder!")
