import os
import random

flag = os.environ.get("FLAG", "tkbctf{dummy}")
random.seed(os.urandom(64))
print([random.random() for _ in range(131)])

happiness = 0
next_val = random.random()
while abs(happiness) < 10**6:
    if float(input()) == next_val:
        print("correct :)")
        happiness += 1
        next_val = random.random()
    else:
        print("incorrect :(")
        happiness -= 1
if happiness < 0:
    print("Too unhappy...")
else:
    print("I'm very happy now! Here is the flag:", flag)
